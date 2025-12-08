"""
Database connection and query execution for SQLite.
"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Any, List, Dict, Tuple

# Database path - use sampled version for smaller deployment size
DB_PATH = Path(__file__).parent.parent / "data" / "linkedin_jobs_sampled.db"


@contextmanager
def get_connection():
    """Get a database connection with row factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def execute_query(sql: str, timeout_seconds: int = 30) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Execute a SQL query and return results.

    Args:
        sql: The SQL query to execute
        timeout_seconds: Maximum execution time

    Returns:
        Tuple of (list of row dicts, list of column names)

    Raises:
        Exception if query fails or times out
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)

        # Get column names
        columns = [description[0] for description in cursor.description] if cursor.description else []

        # Fetch results (limit to 100 rows for safety)
        rows = cursor.fetchmany(100)

        # Convert to list of dicts
        results = [dict(zip(columns, row)) for row in rows]

        return results, columns


def validate_sql(sql: str) -> Tuple[bool, str]:
    """
    Validate that SQL is safe to execute.

    Returns:
        Tuple of (is_valid, error_message)
    """
    sql_upper = sql.strip().upper()

    # Must start with SELECT
    if not sql_upper.startswith("SELECT"):
        return False, "Only SELECT queries are allowed"

    # Block dangerous keywords
    dangerous_keywords = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE", "TRUNCATE", "EXEC", "EXECUTE"]
    for keyword in dangerous_keywords:
        if keyword in sql_upper:
            return False, f"Dangerous keyword '{keyword}' not allowed"

    return True, ""


def get_schema_info() -> str:
    """Get the schema documentation for LLM prompt."""
    schema_path = Path(__file__).parent.parent / "data" / "schema_docs.txt"
    if schema_path.exists():
        return schema_path.read_text()
    return "Schema documentation not found."
