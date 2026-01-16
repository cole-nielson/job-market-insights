"""
Rule-based visualization detection for query results.
Purely deterministic - no LLM calls.
"""

from typing import List, Dict, Any, Optional, Tuple
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


def is_numeric_value(val: Any) -> bool:
    """Check if a value is numeric."""
    return isinstance(val, (int, float)) and not isinstance(val, bool)


def pivot_single_row(
    data: List[Dict[str, Any]],
    columns: List[str]
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Pivot a single row with multiple numeric columns into multiple rows.

    E.g., {entry_pct: 30, senior_pct: 40} becomes:
    [{"category": "entry", "value": 30}, {"category": "senior", "value": 40}]
    """
    row = data[0]
    pivoted = []

    for col in columns:
        val = row.get(col)
        if is_numeric_value(val):
            # Clean up column name for display
            label = col.replace('_pct', '').replace('_percent', '')
            label = label.replace('_count', '').replace('_level', '')
            label = label.replace('_', ' ').title()
            pivoted.append({"category": label, "value": val})

    if len(pivoted) >= 2:
        return pivoted, ["category", "value"]
    return data, columns


def detect_visualization(
    data: Optional[List[Dict[str, Any]]],
    columns: Optional[List[str]]
) -> VisualizationResult:
    """
    Detect the best visualization type for the given data.

    Rules:
    - No data or single value -> "none"
    - Single row with 2+ numeric columns -> pivot and show as pie/bar
    - 2 cols (text + numeric), 2-8 rows -> "pie"
    - 2 cols (text + numeric), 2-20 rows -> "bar"
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

    # Single value case (1 row, 1 column)
    if row_count == 1 and col_count == 1:
        return VisualizationResult(config=VisualizationConfig(type="none"))

    # Single row with multiple numeric columns - try to pivot
    if row_count == 1 and col_count >= 2:
        # Count numeric columns
        row = data[0]
        numeric_cols = [c for c in columns if is_numeric_value(row.get(c))]

        # If we have 2+ numeric columns, pivot them
        if len(numeric_cols) >= 2:
            pivoted_data, pivoted_cols = pivot_single_row(data, columns)
            if len(pivoted_data) >= 2:
                viz_type = "pie" if len(pivoted_data) <= 8 else "bar"
                return VisualizationResult(
                    config=VisualizationConfig(
                        type=viz_type,
                        label_key="category" if viz_type == "pie" else None,
                        x_key="category" if viz_type == "bar" else None,
                        y_key="value"
                    ),
                    data=pivoted_data,
                    columns=pivoted_cols
                )

        return VisualizationResult(config=VisualizationConfig(type="none"))

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
                return VisualizationResult(
                    config=VisualizationConfig(
                        type="pie",
                        label_key=text_col,
                        y_key=num_col
                    )
                )
            # 2-20 rows -> bar chart (good for ranked lists)
            elif row_count <= 20:
                return VisualizationResult(
                    config=VisualizationConfig(
                        type="bar",
                        x_key=text_col,
                        y_key=num_col
                    )
                )

    # More than 20 rows or complex multi-column data -> table
    if row_count > 20 or col_count > 2:
        return VisualizationResult(config=VisualizationConfig(type="table"))

    # Fallback for 2+ rows with 2 columns that aren't text+numeric
    if row_count >= 2:
        return VisualizationResult(config=VisualizationConfig(type="table"))

    return VisualizationResult(config=VisualizationConfig(type="none"))
