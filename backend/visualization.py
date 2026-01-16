"""
Rule-based visualization detection for query results.
Purely deterministic - no LLM calls.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class VisualizationConfig:
    """Configuration for how to visualize query results."""
    type: str  # "bar", "pie", "table", "none"
    x_key: Optional[str] = None
    y_key: Optional[str] = None
    label_key: Optional[str] = None


def is_numeric_column(data: List[Dict[str, Any]], column: str) -> bool:
    """Check if a column contains numeric values."""
    for row in data:
        val = row.get(column)
        if val is not None:
            return isinstance(val, (int, float))
    return False


def is_text_column(data: List[Dict[str, Any]], column: str) -> bool:
    """Check if a column contains text values."""
    for row in data:
        val = row.get(column)
        if val is not None:
            return isinstance(val, str)
    return False


def detect_visualization(
    data: Optional[List[Dict[str, Any]]],
    columns: Optional[List[str]]
) -> VisualizationConfig:
    """
    Detect the best visualization type for the given data.

    Rules:
    - No data or single value -> "none"
    - 2 cols (text + numeric), 2-8 rows -> "pie"
    - 2 cols (text + numeric), 2-20 rows -> "bar"
    - >20 rows or complex data -> "table"

    Args:
        data: List of row dictionaries from query results
        columns: List of column names

    Returns:
        VisualizationConfig with type and relevant keys
    """
    # No data case
    if not data or not columns:
        return VisualizationConfig(type="none")

    row_count = len(data)
    col_count = len(columns)

    # Single value case (1 row, 1 column)
    if row_count == 1 and col_count == 1:
        return VisualizationConfig(type="none")

    # Single row with multiple columns - no chart needed
    if row_count == 1:
        return VisualizationConfig(type="none")

    # Check for 2-column case (text + numeric)
    if col_count == 2:
        col1, col2 = columns[0], columns[1]

        # Determine which is text and which is numeric
        text_col = None
        num_col = None

        if is_text_column(data, col1) and is_numeric_column(data, col2):
            text_col, num_col = col1, col2
        elif is_text_column(data, col2) and is_numeric_column(data, col1):
            text_col, num_col = col2, col1

        if text_col and num_col:
            # 2-8 rows -> pie chart (good for distributions)
            if 2 <= row_count <= 8:
                return VisualizationConfig(
                    type="pie",
                    label_key=text_col,
                    y_key=num_col
                )
            # 2-20 rows -> bar chart (good for ranked lists)
            elif row_count <= 20:
                return VisualizationConfig(
                    type="bar",
                    x_key=text_col,
                    y_key=num_col
                )

    # More than 20 rows or complex multi-column data -> table
    if row_count > 20 or col_count > 2:
        return VisualizationConfig(type="table")

    # Fallback for 2+ rows with 2 columns that aren't text+numeric
    if row_count >= 2:
        return VisualizationConfig(type="table")

    return VisualizationConfig(type="none")
