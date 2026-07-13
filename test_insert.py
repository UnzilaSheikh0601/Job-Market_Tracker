import os
import psycopg2
from dotenv import load_dotenv
 
load_dotenv()
 
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
 
try:
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO jobs (job_title, company, location, search_keyword, description, skills_matched, job_url, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
 
    test_values = (
        "Test Data Analyst",
        "Test Company",
        "Nagpur, India",
        "data analyst",
        "This is a test job description mentioning python and sql.",
        ["python", "sql"],
        "https://example.com/test-job-123",
        "test"
    )

    cursor.execute(insert_query, test_values)
    connection.commit()
 
    print("Test row inserted successfully!")

    cursor.execute("SELECT job_title, company, skills_matched FROM jobs WHERE source = 'test';")
    result = cursor.fetchall()
    print("Data read back from table:", result)
 
    cursor.close()
    connection.close()
 
except Exception as e:
    print("Something went wrong.")
    print("Error:", e)
