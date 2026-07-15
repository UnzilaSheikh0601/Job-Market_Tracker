import os
import ast
import pandas as pd
import numpy as np 
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def clean_value(value):
    if isinstance(value, float) and np.isnan(value):
        return None
    return value

def load_jobs_to_db(csv_path):

    df = pd.read_csv(csv_path)

    df['skills'] = df['skills'].apply(ast.literal_eval)

    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = connection.cursor()

    cursor.execute("SELECT job_url FROM jobs WHERE job_url IS NOT NULL")
    existing_urls = {row[0] for row in cursor.fetchall()}

    insert_query = '''
    INSERT INTO jobs (
        job_title, company, location,
        experience, min_experience, max_experience,
        salary, min_salary, max_salary,
        description, skills_required, posted_duration,
        job_url, search_keyword, source)
    VALUES %s
    ON CONFLICT (job_url) DO NOTHING'''

    all_values = []
    new_urls_seen = set()  
    inserted_count = 0
    skipped_count = 0

    for _, row in df.iterrows():
        job_url = clean_value(row['job_url'])

        if job_url in existing_urls or job_url in new_urls_seen:
            skipped_count += 1
            continue

        values = (
            clean_value(row['title']),
            clean_value(row['company']),
            clean_value(row['location']),
            clean_value(row['experience']),
            clean_value(row['min_experience']),
            clean_value(row['max_experience']),
            clean_value(row['salary']),
            clean_value(row['min_salary']),
            clean_value(row['max_salary']),
            clean_value(row['description']),
            row['skills'],
            clean_value(row['posted_duration']),
            clean_value(row['job_url']),
            clean_value(row['search_keyword']),
            "Naukri"
        )

        all_values.append(values)
        new_urls_seen.add(job_url)
        inserted_count += 1

    if all_values:
        execute_values(cursor, insert_query, all_values)

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Attempted: {len(all_values)} rows")
    print(f"Inserted: {inserted_count} new jobs")
    print(f"Skipped (duplicates): {skipped_count} jobs")

if __name__ == "__main__":
    load_jobs_to_db("data/processed/naukri_jobs_cleaned.csv")