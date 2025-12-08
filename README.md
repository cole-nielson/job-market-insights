# Job Market Insights

A natural language interface for querying LinkedIn job market data. Ask questions in plain English and get AI-powered insights from 120,000+ job postings.

## Features

- **Natural Language Queries**: Ask questions like "What are the most common job titles?" or "What's the average salary for software engineers?"
- **AI-Powered SQL Generation**: Converts your questions to SQL using OpenAI's GPT model
- **Interactive Results**: Get conversational responses with data insights
- **SQL Transparency**: Optionally view the generated SQL queries

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React + TypeScript + Tailwind CSS + shadcn/ui
- **Database**: SQLite (120K+ LinkedIn job postings)
- **AI**: OpenAI GPT API

## Data Source

This project uses the [LinkedIn Job Postings dataset from Kaggle](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings).

The database is not included in this repository due to size. See setup instructions below.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/cole-nielson/job-market-insights.git
cd job-market-insights
```

### 2. Set up the database

**Option A: Automatic download from Kaggle**

1. Create a Kaggle account and get your API credentials from [kaggle.com/settings](https://www.kaggle.com/settings)
2. Set environment variables:
   ```bash
   export KAGGLE_USERNAME=your_username
   export KAGGLE_KEY=your_api_key
   ```
3. Run the setup script:
   ```bash
   pip install kaggle pandas
   python scripts/setup_data.py
   ```

**Option B: Manual download**

1. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings)
2. Extract to the `data/` directory
3. Run the database creation script:
   ```bash
   pip install pandas
   python scripts/create_database.py
   ```

### 3. Set up the backend

```bash
cd backend
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY=your_openai_api_key

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Set up the frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at http://localhost:5173

## Deployment

### Backend (Render)

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Set environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `KAGGLE_USERNAME`: Your Kaggle username
   - `KAGGLE_KEY`: Your Kaggle API key
4. Set build command: `pip install -r backend/requirements.txt && pip install kaggle pandas && python scripts/setup_data.py`
5. Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)

1. Import your repository on [Vercel](https://vercel.com)
2. Set root directory to `frontend`
3. Set environment variable:
   - `VITE_API_URL`: Your Render backend URL

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI app
│   ├── database.py          # SQLite connection
│   ├── llm.py               # OpenAI integration
│   ├── query_pipeline.py    # NL → SQL → NL pipeline
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── App.tsx          # Main React component
│   └── package.json
├── scripts/
│   ├── create_database.py   # CSV → SQLite loader
│   └── setup_data.py        # Kaggle download + setup
└── data/
    └── schema_docs.txt      # Schema documentation for LLM
```

## Example Queries

- "What are the most common job titles?"
- "What's the average salary for software engineers?"
- "Which companies have the most job postings?"
- "How many remote jobs are available?"
- "What industries have the most job openings?"
- "What percentage of jobs are entry-level vs senior?"
