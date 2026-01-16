"""
FastAPI application for NL-to-SQL job market insights.
"""

import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from query_pipeline import process_query
from visualization import detect_visualization

app = FastAPI(
    title="Job Market Insights API",
    description="Natural language interface for querying LinkedIn job market data",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    """Request body for query endpoint."""
    question: str


class VisualizationConfigModel(BaseModel):
    """Configuration for data visualization."""
    type: str  # "bar", "pie", "table", "none"
    x_key: Optional[str] = None
    y_key: Optional[str] = None
    label_key: Optional[str] = None


class QueryResponse(BaseModel):
    """Response body for query endpoint."""
    success: bool
    response: str
    sql: str
    error: Optional[str] = None
    data: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None
    visualization: Optional[VisualizationConfigModel] = None


class ExampleQuery(BaseModel):
    """An example query for the UI."""
    question: str
    category: str


# Example queries for the UI
EXAMPLE_QUERIES = [
    ExampleQuery(
        question="What are the most common job titles?",
        category="Titles"
    ),
    ExampleQuery(
        question="What's the average salary for software engineers?",
        category="Salary"
    ),
    ExampleQuery(
        question="Which companies have the most job postings?",
        category="Companies"
    ),
    ExampleQuery(
        question="How many remote jobs are available?",
        category="Remote"
    ),
    ExampleQuery(
        question="What industries have the most job openings?",
        category="Industries"
    ),
    ExampleQuery(
        question="What percentage of jobs are entry-level vs senior?",
        category="Experience"
    ),
]


@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Job Market Insights API"}


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Process a natural language question about job market data.

    The system will:
    1. Convert your question to SQL
    2. Execute the query against the database
    3. Return insights in natural language
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if len(request.question) > 500:
        raise HTTPException(status_code=400, detail="Question too long (max 500 characters)")

    result = process_query(request.question)

    # Detect visualization type (may transform data for pivoted single-row results)
    viz_result = detect_visualization(result.raw_results, result.columns)

    # Use transformed data if available, otherwise use original
    chart_data = viz_result.data if viz_result.data is not None else result.raw_results
    chart_columns = viz_result.columns if viz_result.columns is not None else result.columns

    return QueryResponse(
        success=result.success,
        response=result.response,
        sql=result.sql,
        error=result.error,
        data=chart_data,
        columns=chart_columns,
        visualization=VisualizationConfigModel(
            type=viz_result.config.type,
            x_key=viz_result.config.x_key,
            y_key=viz_result.config.y_key,
            label_key=viz_result.config.label_key
        )
    )


@app.get("/examples", response_model=List[ExampleQuery])
async def get_examples():
    """Get example queries for the UI."""
    return EXAMPLE_QUERIES


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
