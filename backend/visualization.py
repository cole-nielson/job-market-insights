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


@dataclass
class VisualizationResult:
    """Result containing config and potentially transformed data."""
    config: VisualizationConfig
    data: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None


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
) -> VisualizationResult:
    """
    Detect the best visualization type for the given data.

    Rules:
    - No data or single row -> "none" (text is sufficient)
    - 2 cols (text + numeric), 2-8 rows -> "pie"
    - 2 cols (text + numeric), 9-20 rows -> "bar"
    - >20 rows or complex data -> "table"

    Args:
        data: List of row dictionaries from query results
        columns: List of column names

    Returns:
        VisualizationResult with config and potentially transformed data
    """
    # No data case
    if not data or not columns:
        return VisualizationResult(config=VisualizationConfig(type="none"))

    row_count = len(data)
    col_count = len(columns)

    # Single row results - no chart needed, text response is sufficient
    # This avoids nonsensical charts like comparing salary ($139k) vs count (16)
    if row_count == 1:
        return VisualizationResult(config=VisualizationConfig(type="none"))

    # Find text and numeric columns
    text_cols = [c for c in columns if is_text_column(data, c)]
    num_cols = [c for c in columns if is_numeric_column(data, c)]

    # If we have at least one text column and one numeric column, we can chart
    if text_cols and num_cols:
        label_col = text_cols[0]
        # Prefer count columns over percentage columns for chart values
        value_col = num_cols[0]
        for nc in num_cols:
            nc_lower = nc.lower()
            if 'count' in nc_lower or 'total' in nc_lower or 'num' in nc_lower:
                value_col = nc
                break

        # 2-8 rows -> pie chart (good for distributions)
        if 2 <= row_count <= 8:
            return VisualizationResult(
                config=VisualizationConfig(
                    type="pie",
                    label_key=label_col,
                    y_key=value_col
                )
            )
        # 9-20 rows -> bar chart (good for ranked lists)
        elif row_count <= 20:
            return VisualizationResult(
                config=VisualizationConfig(
                    type="bar",
                    x_key=label_col,
                    y_key=value_col
                )
            )

    # More than 20 rows -> table
    if row_count > 20:
        return VisualizationResult(config=VisualizationConfig(type="table"))

    # Fallback for data that couldn't be charted
    if row_count >= 2:
        return VisualizationResult(config=VisualizationConfig(type="table"))

    return VisualizationResult(config=VisualizationConfig(type="none"))
