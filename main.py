import pandas as pd
from scraper.naukri_scraper import scrape_naukri_jobs
from pipeline.clean import clean_jobs_csv
from pipeline.load_to_db import load_jobs_to_db

TARGET_SEARCHES = [
    ("data analyst", "data-analyst-jobs"),
    ("business analyst", "business-analyst-jobs"),
    ("python developer", "python-developer-jobs"),
    ("data engineer", "data-engineer-jobs"),
    ("mis executive", "mis-executive-jobs"),
    ("reporting analyst", "reporting-analyst-jobs"),
]

RAW_CSV_PATH = "data/raw/naukri_jobs.csv"
CLEANED_CSV_PATH = "data/processed/naukri_jobs_cleaned.csv"

if __name__ == "__main__":
    all_jobs = []

    for search_keyword, url_slug in TARGET_SEARCHES:
        jobs = scrape_naukri_jobs(search_keyword, url_slug, num_pages=5)
        all_jobs.extend(jobs)
        pd.DataFrame(jobs).to_csv(f"data/raw/search_keyword_csvs/{search_keyword}.csv", index=False)

    pd.DataFrame(all_jobs).to_csv(RAW_CSV_PATH, index=False)  

    print(f"\nDone. Total jobs scraped: {len(all_jobs)}")
    print(f"Saved raw data to {RAW_CSV_PATH}")

    df = pd.read_csv("data/raw/naukri_jobs.csv")

    # Find job_urls that appear more than once
    duplicate_urls = df[df.duplicated(subset="job_url", keep=False)]
    print(f"Total duplicate rows: {len(duplicate_urls)}")

    # Show which search_keywords these duplicates came from
    print(duplicate_urls.groupby("job_url")["search_keyword"].apply(list).head(20))
    
    clean_jobs_csv(RAW_CSV_PATH, CLEANED_CSV_PATH)
    print(f"Processed raw data of {RAW_CSV_PATH} into {CLEANED_CSV_PATH}")

    print("\nLoading data to DB")
    load_jobs_to_db(CLEANED_CSV_PATH)
    print("Loaded data to DB")