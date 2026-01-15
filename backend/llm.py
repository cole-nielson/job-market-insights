"""
OpenAI LLM integration for SQL generation and response formatting.
"""

import os
from typing import List, Dict
from openai import OpenAI

# Initialize client (API key from environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-5-mini-2025-08-07"

# Token limits for reasoning model - needs higher limits to account for
# internal reasoning tokens that are consumed before generating visible output
SQL_GENERATION_TOKENS = 1500
RESPONSE_FORMATTING_TOKENS = 2500


def generate_sql(question: str, schema: str) -> str:
    """
    Generate SQL query from natural language question.

    Args:
        question: User's natural language question
        schema: Database schema documentation

    Returns:
        Generated SQL query string
    """
    system_prompt = f"""You are an expert SQL query generator. Your task is to convert natural language questions into valid SQLite queries.

{schema}

IMPORTANT RULES:
1. Generate ONLY the SQL query - no explanations, no markdown formatting, no code blocks
2. Use only SELECT statements
3. Always use LIMIT to cap results (max 100 rows)
4. Use appropriate JOINs when data spans multiple tables
5. CRITICAL: The "skills" table contains JOB FUNCTIONS (like "Information Technology", "Sales", "Management"), NOT technical skills (like "Python", "SQL"). When users ask about "skills", query the skills table but the results are job function categories.
6. For industry lookups, join job_industries with industries table using industry_id
7. Use LIKE with wildcards for text searches on job titles (e.g., title LIKE '%data scientist%')
8. The postings table has salary info (max_salary, med_salary, min_salary) - use these for salary questions
9. For remote jobs, check remote_allowed = 1
10. Experience levels are in formatted_experience_level column

If the question cannot be answered with the available data, return:
SELECT 'This question cannot be answered with the available data.' as message"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        max_completion_tokens=SQL_GENERATION_TOKENS
    )

    sql = response.choices[0].message.content
    if not sql:
        raise ValueError("LLM returned empty SQL response")

    sql = sql.strip()

    # Clean up any markdown formatting if present
    if sql.startswith("```"):
        lines = sql.split("\n")
        sql = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

    return sql


def generate_sql_with_error_retry(question: str, schema: str, error_sql: str, error_message: str) -> str:
    """
    Retry SQL generation with error context.

    Args:
        question: Original question
        schema: Database schema
        error_sql: The SQL that failed
        error_message: The error message

    Returns:
        New SQL query attempt
    """
    system_prompt = f"""You are an expert SQL query generator. Your previous SQL query failed. Generate a corrected query.

{schema}

PREVIOUS FAILED QUERY:
{error_sql}

ERROR MESSAGE:
{error_message}

Generate a corrected SQL query that fixes this error. Return ONLY the SQL query - no explanations."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        max_completion_tokens=SQL_GENERATION_TOKENS
    )

    sql = response.choices[0].message.content
    if not sql:
        raise ValueError("LLM returned empty SQL response on retry")

    sql = sql.strip()

    # Clean up any markdown formatting if present
    if sql.startswith("```"):
        lines = sql.split("\n")
        sql = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

    return sql


def format_response(question: str, results: List[Dict], columns: List[str]) -> str:
    """
    Convert SQL results into natural language response.

    Args:
        question: Original question
        results: Query results as list of dicts
        columns: Column names

    Returns:
        Natural language response
    """
    if not results:
        return "No results found for your query. The data might not contain information matching your criteria."

    # Check for error message response
    if len(results) == 1 and "message" in results[0]:
        return results[0]["message"]

    # Truncate results for prompt if too many
    results_for_prompt = results[:50]

    # Format results as readable text
    results_text = f"Columns: {', '.join(columns)}\n\nResults ({len(results)} rows):\n"
    for i, row in enumerate(results_for_prompt, 1):
        row_text = ", ".join(f"{k}: {v}" for k, v in row.items())
        results_text += f"{i}. {row_text}\n"

    if len(results) > 50:
        results_text += f"... and {len(results) - 50} more rows"

    system_prompt = """You are a helpful data analyst assistant. Convert these SQL query results into a clear, conversational response.

RULES:
1. Be concise but informative
2. Include specific numbers and data points
3. Format lists nicely when appropriate
4. Don't mention SQL or databases - just present the insights naturally
5. If showing rankings or top items, format them as a numbered list
6. IMPORTANT: If the results contain skill_name data, these are actually JOB FUNCTION CATEGORIES (like "Information Technology", "Sales"), not technical skills. Refer to them as "job functions" or "job categories" rather than "skills"."""

    user_prompt = f"""Question: {question}

{results_text}

Provide a natural language response summarizing these results."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_completion_tokens=RESPONSE_FORMATTING_TOKENS
    )

    content = response.choices[0].message.content
    if not content:
        # Fallback if LLM returns empty content
        return f"Found {len(results)} results for your query."

    return content.strip()
