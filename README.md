# Job Market Insights

**Natural Language Interface for Job Market Analytics**

Ask questions about the job market in plain English and get AI-powered insights from 123,000+ LinkedIn job postings. No SQL knowledge required.

[Live Demo](https://job-market-insights-lac.vercel.app) | [Backend API](https://job-market-insights.onrender.com/docs)

---

## Overview

Job Market Insights makes labor market data accessible to anyone. Instead of writing complex SQL queries, users can ask natural language questions like "What's the average salary for data scientists?" or "Which industries are hiring the most?" The system translates these questions into SQL, executes them against a database of LinkedIn job postings, and returns conversational insights.

### Key Features

- **Natural Language Queries** - Ask questions in plain English about salaries, companies, industries, and job trends
- **AI-Powered SQL Generation** - Converts questions to optimized SQL using OpenAI's GPT with automatic error recovery
- **SQL Transparency** - Optionally view the generated SQL to understand how your question was interpreted
- **Schema-Aware Prompting** - LLM receives detailed schema documentation to generate accurate queries
- **Query Validation** - Built-in SQL validation prevents injection attacks and dangerous operations

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                    │
│                         (Vercel - React/Vite)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Search    │  │   Example   │  │   Results   │  │     SQL     │    │
│  │    Input    │  │   Queries   │  │   Display   │  │   Viewer    │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ REST API
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          BACKEND API                                     │
│                      (Render - FastAPI)                                  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                      Query Pipeline                               │   │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────────────┐  │   │
│  │  │ Question│──▶│Generate │──▶│Validate │──▶│Execute + Retry  │  │   │
│  │  │  Input  │   │   SQL   │   │   SQL   │   │   if Failed     │  │   │
│  │  └─────────┘   └─────────┘   └─────────┘   └────────┬────────┘  │   │
│  │                                                      │           │   │
│  │                              ┌───────────────────────┘           │   │
│  │                              ▼                                   │   │
│  │                       ┌─────────────┐   ┌─────────────┐         │   │
│  │                       │   Format    │──▶│   Return    │         │   │
│  │                       │  Response   │   │   Insights  │         │   │
│  │                       └─────────────┘   └─────────────┘         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────┐                        ┌──────────────────────────┐   │
│  │   OpenAI     │                        │        SQLite            │   │
│  │   GPT API    │                        │  (123K Job Postings)     │   │
│  └──────────────┘                        └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 19** | UI framework |
| **TypeScript** | Type safety |
| **Vite** | Build tool & dev server |
| **Tailwind CSS** | Utility-first styling |
| **shadcn/ui** | Component library (Radix primitives) |
| **Lucide React** | Icon library |

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Async Python web framework |
| **OpenAI API** | GPT for SQL generation and response formatting |
| **SQLite** | Embedded database (123K+ job postings) |
| **Pydantic** | Request/response validation |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| **Render** | Backend hosting with persistent disk |
| **Vercel** | Frontend hosting |
| **GitHub Releases** | Database file distribution |

---

## Technical Highlights

### 1. Multi-Stage Query Pipeline with Error Recovery

The core of the application is a pipeline that converts natural language to SQL, executes it, and formats results back to natural language. If the initial SQL fails, it automatically retries with error context:

```python
def process_query(question: str) -> QueryResult:
    schema = get_schema_info()

    # Step 1: Generate SQL from natural language
    sql = generate_sql(question, schema)

    # Step 2: Validate SQL (prevent injection, only SELECT allowed)
    is_valid, validation_error = validate_sql(sql)
    if not is_valid:
        return QueryResult(success=False, error=validation_error)

    # Step 3: Execute SQL
    try:
        results, columns = execute_query(sql)
    except Exception as e:
        # Step 4: Retry with error context
        sql = generate_sql_with_error_retry(question, schema, sql, str(e))
        results, columns = execute_query(sql)

    # Step 5: Format results as natural language
    response = format_response(question, results, columns)
    return QueryResult(success=True, response=response, sql=sql)
```

### 2. Schema-Aware SQL Generation

The LLM receives comprehensive schema documentation including table relationships, column descriptions, and important caveats. This context enables accurate query generation:

```python
system_prompt = f"""You are an expert SQL query generator.

{schema}  # Full schema with relationships and notes

IMPORTANT RULES:
1. Generate ONLY the SQL query - no explanations
2. Use only SELECT statements
3. Always use LIMIT to cap results (max 100 rows)
4. Use appropriate JOINs when data spans multiple tables
5. The "skills" table contains JOB FUNCTIONS, not technical skills
6. For remote jobs, check remote_allowed = 1
..."""
```

### 3. SQL Injection Prevention

All generated SQL is validated before execution to prevent dangerous operations:

```python
def validate_sql(sql: str) -> Tuple[bool, str]:
    sql_upper = sql.strip().upper()

    # Must start with SELECT
    if not sql_upper.startswith("SELECT"):
        return False, "Only SELECT queries are allowed"

    # Block dangerous keywords
    dangerous = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER",
                 "CREATE", "TRUNCATE", "EXEC", "EXECUTE"]
    for keyword in dangerous:
        if keyword in sql_upper:
            return False, f"Dangerous keyword '{keyword}' not allowed"

    return True, ""
```

### 4. Conversational Response Formatting

Raw SQL results are transformed into natural language insights, making data accessible to non-technical users:

```python
system_prompt = """Convert SQL query results into a clear, conversational response.

RULES:
1. Be concise but informative
2. Include specific numbers and data points
3. Format lists nicely when appropriate
4. Don't mention SQL or databases - just present insights naturally
5. If showing rankings, format as a numbered list"""
```

---

## Database Schema

The SQLite database contains 123,000+ LinkedIn job postings with 11 related tables:

| Table | Rows | Description |
|-------|------|-------------|
| `postings` | 123,849 | Main job listings with title, salary, location, experience level |
| `companies` | 24,473 | Company information and descriptions |
| `salaries` | 40,785 | Detailed salary breakdowns by job |
| `benefits` | 67,943 | Job benefits (health insurance, 401k, etc.) |
| `industries` | 422 | Industry categories |
| `skills` | 35 | Job function categories |
| `job_industries` | 164,808 | Links jobs to industries |
| `job_skills` | 213,768 | Links jobs to functions |
| `employee_counts` | 35,787 | Company size over time |

---

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/cole-nielson/job-market-insights.git
   cd job-market-insights
   ```

2. **Set up the database**

   **Option A: Download from GitHub Releases**
   ```bash
   # Download the pre-built database
   curl -L https://github.com/cole-nielson/job-market-insights/releases/download/v1.0.0/linkedin_jobs.db -o data/linkedin_jobs.db
   ```

   **Option B: Build from Kaggle data**
   ```bash
   # Set Kaggle credentials
   export KAGGLE_USERNAME=your_username
   export KAGGLE_KEY=your_api_key

   # Download and build
   pip install kaggle pandas
   python scripts/setup_data.py
   ```

3. **Start the backend**
   ```bash
   cd backend
   pip install -r requirements.txt

   # Set your OpenAI API key
   export OPENAI_API_KEY=your_openai_api_key

   # Run the server
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

4. **Start the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/query` | Submit a natural language question |
| `GET` | `/examples` | Get example queries for the UI |
| `GET` | `/` | Health check endpoint |

### Query Endpoint

**Request:**
```json
{
  "question": "What are the top 5 companies by job postings?"
}
```

**Response:**
```json
{
  "success": true,
  "response": "The top 5 companies by job postings are:\n1. Amazon - 342 postings\n2. Google - 287 postings\n...",
  "sql": "SELECT company_name, COUNT(*) as count FROM postings GROUP BY company_name ORDER BY count DESC LIMIT 5",
  "error": null
}
```

---

## Project Structure

```
job-market-insights/
├── backend/
│   ├── main.py              # FastAPI app with routes
│   ├── database.py          # SQLite connection & query execution
│   ├── llm.py               # OpenAI integration for SQL & NL generation
│   ├── query_pipeline.py    # NL → SQL → NL orchestration
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   ├── components/ui/   # shadcn/ui components
│   │   └── lib/utils.ts     # Tailwind utilities
│   ├── package.json
│   └── vite.config.ts
│
├── scripts/
│   ├── create_database.py   # CSV → SQLite loader with indexing
│   └── setup_data.py        # Kaggle download + database setup
│
├── data/
│   ├── linkedin_jobs.db     # SQLite database (via GitHub Releases)
│   └── schema_docs.txt      # Schema documentation for LLM
│
└── README.md
```

---

## Deployment

### Backend (Render)
Auto-deploys from `main` branch:
- Build: `pip install -r backend/requirements.txt && pip install kaggle pandas && python scripts/setup_data.py`
- Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- Env: `OPENAI_API_KEY`, `KAGGLE_USERNAME`, `KAGGLE_KEY`

### Frontend (Vercel)
Auto-deploys from `main` branch:
- Root directory: `frontend`
- Build: `npm run build`
- Env: `VITE_API_URL` pointing to Render backend

---

## Example Queries

| Category | Example Question |
|----------|------------------|
| **Salary** | "What's the average salary for software engineers?" |
| **Companies** | "Which companies have the most job postings?" |
| **Remote** | "How many remote jobs are available?" |
| **Industries** | "What industries have the most job openings?" |
| **Experience** | "What percentage of jobs are entry-level vs senior?" |
| **Trends** | "What are the most common job titles?" |

---

## Future Improvements

- [ ] Add conversation history for follow-up questions
- [ ] Implement caching for common queries
- [ ] Add data visualizations (charts, graphs)
- [ ] Support date-range filtering
- [ ] Add query suggestions based on partial input
- [ ] Implement rate limiting for API protection

---

## Data Source

This project uses the [LinkedIn Job Postings dataset from Kaggle](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) (2023-2024).

---

## License

MIT License

---

## Author

**Cole Nielson**
- [GitHub](https://github.com/cole-nielson)
- [LinkedIn](https://www.linkedin.com/in/cole-nielson-b05724196/)
