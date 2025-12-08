"""
Create SQLite database from LinkedIn job postings CSV files.
Loads all 11 tables with proper types and creates indexes for query performance.
"""

import sqlite3
import pandas as pd
from pathlib import Path
import sys

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "linkedin_jobs.db"

# Table definitions with their CSV paths and column types
TABLES = {
    "postings": {
        "csv": DATA_DIR / "postings.csv",
        "dtypes": {
            "job_id": "Int64",
            "company_id": "Int64",
            "views": "Int64",
            "applies": "Int64",
            "remote_allowed": "Int64",
            "sponsored": "Int64",
        }
    },
    "companies": {
        "csv": DATA_DIR / "companies" / "companies.csv",
        "dtypes": {"company_id": "Int64"}
    },
    "employee_counts": {
        "csv": DATA_DIR / "companies" / "employee_counts.csv",
        "dtypes": {"company_id": "Int64", "employee_count": "Int64", "follower_count": "Int64"}
    },
    "company_industries": {
        "csv": DATA_DIR / "companies" / "company_industries.csv",
        "dtypes": {"company_id": "Int64"}
    },
    "company_specialities": {
        "csv": DATA_DIR / "companies" / "company_specialities.csv",
        "dtypes": {"company_id": "Int64"}
    },
    "benefits": {
        "csv": DATA_DIR / "jobs" / "benefits.csv",
        "dtypes": {"job_id": "Int64", "inferred": "Int64"}
    },
    "salaries": {
        "csv": DATA_DIR / "jobs" / "salaries.csv",
        "dtypes": {"salary_id": "Int64", "job_id": "Int64"}
    },
    "job_industries": {
        "csv": DATA_DIR / "jobs" / "job_industries.csv",
        "dtypes": {"job_id": "Int64", "industry_id": "Int64"}
    },
    "job_skills": {
        "csv": DATA_DIR / "jobs" / "job_skills.csv",
        "dtypes": {"job_id": "Int64"}
    },
    "skills": {
        "csv": DATA_DIR / "mappings" / "skills.csv",
        "dtypes": {}
    },
    "industries": {
        "csv": DATA_DIR / "mappings" / "industries.csv",
        "dtypes": {"industry_id": "Int64"}
    },
}

# Indexes to create for query performance
INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_postings_job_id ON postings(job_id)",
    "CREATE INDEX IF NOT EXISTS idx_postings_company_id ON postings(company_id)",
    "CREATE INDEX IF NOT EXISTS idx_postings_title ON postings(title)",
    "CREATE INDEX IF NOT EXISTS idx_postings_location ON postings(location)",
    "CREATE INDEX IF NOT EXISTS idx_postings_experience ON postings(formatted_experience_level)",
    "CREATE INDEX IF NOT EXISTS idx_postings_remote ON postings(remote_allowed)",
    "CREATE INDEX IF NOT EXISTS idx_companies_company_id ON companies(company_id)",
    "CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(name)",
    "CREATE INDEX IF NOT EXISTS idx_job_skills_job_id ON job_skills(job_id)",
    "CREATE INDEX IF NOT EXISTS idx_job_skills_skill ON job_skills(skill_abr)",
    "CREATE INDEX IF NOT EXISTS idx_job_industries_job_id ON job_industries(job_id)",
    "CREATE INDEX IF NOT EXISTS idx_job_industries_industry ON job_industries(industry_id)",
    "CREATE INDEX IF NOT EXISTS idx_salaries_job_id ON salaries(job_id)",
    "CREATE INDEX IF NOT EXISTS idx_benefits_job_id ON benefits(job_id)",
    "CREATE INDEX IF NOT EXISTS idx_employee_counts_company_id ON employee_counts(company_id)",
]


def load_csv_to_sqlite(table_name: str, config: dict, conn: sqlite3.Connection) -> int:
    """Load a CSV file into SQLite table."""
    csv_path = config["csv"]
    dtypes = config.get("dtypes", {})

    print(f"Loading {table_name} from {csv_path.name}...", end=" ", flush=True)

    # Read CSV with pandas (handles quoted fields with newlines properly)
    df = pd.read_csv(csv_path, dtype=dtypes, low_memory=False)

    # Write to SQLite
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    row_count = len(df)
    print(f"{row_count:,} rows")
    return row_count


def create_indexes(conn: sqlite3.Connection):
    """Create indexes for query performance."""
    print("\nCreating indexes...")
    cursor = conn.cursor()
    for idx_sql in INDEXES:
        idx_name = idx_sql.split()[5]  # Extract index name
        print(f"  {idx_name}")
        cursor.execute(idx_sql)
    conn.commit()


def generate_schema_docs(conn: sqlite3.Connection) -> str:
    """Generate schema documentation for LLM prompt."""
    cursor = conn.cursor()

    schema_docs = []
    schema_docs.append("DATABASE SCHEMA")
    schema_docs.append("=" * 50)

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()

        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        row_count = cursor.fetchone()[0]

        schema_docs.append(f"\nTable: {table} ({row_count:,} rows)")
        schema_docs.append("-" * 40)
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            schema_docs.append(f"  - {col_name} ({col_type})")

    # Add relationship documentation
    schema_docs.append("\n" + "=" * 50)
    schema_docs.append("TABLE RELATIONSHIPS")
    schema_docs.append("=" * 50)
    schema_docs.append("""
- postings.company_id -> companies.company_id
- postings.job_id -> job_skills.job_id -> skills.skill_abr
- postings.job_id -> job_industries.job_id -> industries.industry_id
- postings.job_id -> benefits.job_id
- postings.job_id -> salaries.job_id
- companies.company_id -> employee_counts.company_id
- companies.company_id -> company_industries.company_id
- companies.company_id -> company_specialities.company_id
""")

    return "\n".join(schema_docs)


def main():
    # Remove existing database
    if DB_PATH.exists():
        print(f"Removing existing database: {DB_PATH}")
        DB_PATH.unlink()

    print(f"Creating database: {DB_PATH}\n")

    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)

    total_rows = 0

    # Load all tables
    for table_name, config in TABLES.items():
        try:
            rows = load_csv_to_sqlite(table_name, config, conn)
            total_rows += rows
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)

    # Create indexes
    create_indexes(conn)

    # Generate and save schema documentation
    schema_docs = generate_schema_docs(conn)
    schema_path = DATA_DIR / "schema_docs.txt"
    with open(schema_path, "w") as f:
        f.write(schema_docs)
    print(f"\nSchema documentation saved to: {schema_path}")

    # Final stats
    conn.close()
    db_size_mb = DB_PATH.stat().st_size / (1024 * 1024)

    print(f"\n{'=' * 50}")
    print(f"Database created successfully!")
    print(f"Total rows: {total_rows:,}")
    print(f"Database size: {db_size_mb:.1f} MB")
    print(f"Location: {DB_PATH}")


if __name__ == "__main__":
    main()
