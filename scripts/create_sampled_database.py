"""
Create a sampled SQLite database for deployment.
Reduces the postings table to 30K rows to keep file size manageable.
"""

import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
SOURCE_DB = DATA_DIR / "linkedin_jobs.db"
SAMPLED_DB = DATA_DIR / "linkedin_jobs_sampled.db"

SAMPLE_SIZE = 15000  # Number of postings to keep (smaller for GitHub)


def create_sampled_db():
    print(f"Creating sampled database with {SAMPLE_SIZE} postings...")

    # Remove existing sampled database
    if SAMPLED_DB.exists():
        SAMPLED_DB.unlink()

    # Connect to source
    source = sqlite3.connect(SOURCE_DB)
    source.row_factory = sqlite3.Row

    # Create new database
    dest = sqlite3.connect(SAMPLED_DB)

    # Get random sample of job_ids
    print("Sampling job postings...")
    cursor = source.cursor()
    cursor.execute(f"SELECT job_id FROM postings ORDER BY RANDOM() LIMIT {SAMPLE_SIZE}")
    sampled_job_ids = [row[0] for row in cursor.fetchall()]
    job_ids_str = ",".join(str(id) for id in sampled_job_ids)

    # Copy postings (sampled)
    print("Copying sampled postings...")
    source.execute("ATTACH DATABASE ? AS dest", (str(SAMPLED_DB),))
    source.execute(f"""
        CREATE TABLE dest.postings AS
        SELECT * FROM postings WHERE job_id IN ({job_ids_str})
    """)

    # Copy related tables (filtered by sampled job_ids)
    print("Copying related job tables...")
    source.execute(f"""
        CREATE TABLE dest.job_skills AS
        SELECT * FROM job_skills WHERE job_id IN ({job_ids_str})
    """)
    source.execute(f"""
        CREATE TABLE dest.job_industries AS
        SELECT * FROM job_industries WHERE job_id IN ({job_ids_str})
    """)
    source.execute(f"""
        CREATE TABLE dest.benefits AS
        SELECT * FROM benefits WHERE job_id IN ({job_ids_str})
    """)
    source.execute(f"""
        CREATE TABLE dest.salaries AS
        SELECT * FROM salaries WHERE job_id IN ({job_ids_str})
    """)

    # Get sampled company_ids
    cursor.execute(f"SELECT DISTINCT company_id FROM postings WHERE job_id IN ({job_ids_str})")
    company_ids = [row[0] for row in cursor.fetchall() if row[0]]
    company_ids_str = ",".join(str(id) for id in company_ids)

    # Copy company tables (filtered)
    print("Copying company tables...")
    source.execute(f"""
        CREATE TABLE dest.companies AS
        SELECT * FROM companies WHERE company_id IN ({company_ids_str})
    """)
    source.execute(f"""
        CREATE TABLE dest.employee_counts AS
        SELECT * FROM employee_counts WHERE company_id IN ({company_ids_str})
    """)
    source.execute(f"""
        CREATE TABLE dest.company_industries AS
        SELECT * FROM company_industries WHERE company_id IN ({company_ids_str})
    """)
    source.execute(f"""
        CREATE TABLE dest.company_specialities AS
        SELECT * FROM company_specialities WHERE company_id IN ({company_ids_str})
    """)

    # Copy reference tables (full)
    print("Copying reference tables...")
    source.execute("CREATE TABLE dest.skills AS SELECT * FROM skills")
    source.execute("CREATE TABLE dest.industries AS SELECT * FROM industries")

    source.commit()
    source.close()

    # Create indexes on new database
    print("Creating indexes...")
    dest_cursor = dest.cursor()
    indexes = [
        "CREATE INDEX idx_postings_job_id ON postings(job_id)",
        "CREATE INDEX idx_postings_company_id ON postings(company_id)",
        "CREATE INDEX idx_postings_title ON postings(title)",
        "CREATE INDEX idx_job_skills_job_id ON job_skills(job_id)",
        "CREATE INDEX idx_job_skills_skill ON job_skills(skill_abr)",
        "CREATE INDEX idx_job_industries_job_id ON job_industries(job_id)",
        "CREATE INDEX idx_companies_company_id ON companies(company_id)",
    ]
    for idx in indexes:
        dest_cursor.execute(idx)
    dest.commit()

    # Vacuum to optimize file size
    print("Optimizing database...")
    dest.execute("VACUUM")
    dest.close()

    # Report stats
    size_mb = SAMPLED_DB.stat().st_size / (1024 * 1024)
    print(f"\nSampled database created: {SAMPLED_DB}")
    print(f"Size: {size_mb:.1f} MB")


if __name__ == "__main__":
    create_sampled_db()
