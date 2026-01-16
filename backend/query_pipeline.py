"""
Query pipeline: Natural Language -> SQL -> Execute -> Natural Language Response
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from database import execute_query, validate_sql, get_schema_info
from llm import generate_sql, generate_sql_with_error_retry, format_response


@dataclass
class QueryResult:
    """Result of a query pipeline execution."""
    success: bool
    response: str
    sql: str
    error: Optional[str] = None
    raw_results: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None


def process_query(question: str) -> QueryResult:
    """
    Process a natural language question through the full pipeline.

    1. Generate SQL from question
    2. Validate SQL
    3. Execute SQL
    4. If error, retry once
    5. Format results as natural language

    Args:
        question: User's natural language question

    Returns:
        QueryResult with response, SQL, and status
    """
    schema = get_schema_info()

    # Step 1: Generate SQL
    try:
        sql = generate_sql(question, schema)
    except Exception as e:
        return QueryResult(
            success=False,
            response="I encountered an error generating the query. Please try rephrasing your question.",
            sql="",
            error=str(e)
        )

    # Step 2: Validate SQL
    is_valid, validation_error = validate_sql(sql)
    if not is_valid:
        return QueryResult(
            success=False,
            response=f"I generated an unsafe query. Please try a different question.",
            sql=sql,
            error=validation_error
        )

    # Step 3: Execute SQL
    try:
        results, columns = execute_query(sql)
    except Exception as e:
        # Step 4: Retry once with error context
        try:
            sql = generate_sql_with_error_retry(question, schema, sql, str(e))

            # Validate retry
            is_valid, validation_error = validate_sql(sql)
            if not is_valid:
                return QueryResult(
                    success=False,
                    response="I couldn't generate a valid query for your question. Please try rephrasing.",
                    sql=sql,
                    error=validation_error
                )

            results, columns = execute_query(sql)
        except Exception as retry_error:
            return QueryResult(
                success=False,
                response="I had trouble executing the query. This might be because the requested data doesn't exist in the database, or the question is too complex. Please try a simpler question.",
                sql=sql,
                error=str(retry_error)
            )

    # Step 5: Format response
    try:
        response = format_response(question, results, columns)
    except Exception as e:
        # If formatting fails, return raw results summary
        response = f"Found {len(results)} results, but had trouble formatting the response."

    return QueryResult(
        success=True,
        response=response,
        sql=sql,
        raw_results=results,
        columns=columns
    )
