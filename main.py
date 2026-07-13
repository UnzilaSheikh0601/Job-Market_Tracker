import pandas as pd
from scraper.naukri_scraper import scrape_naukri_jobs

TARGET_SEARCHES = [
    ("data analyst", "data-analyst-jobs"),
    # ("business analyst", "business-analyst-jobs"),
    # ("python developer", "python-developer-jobs"),
    # ("data engineer", "data-engineer-jobs"),
    # ("mis executive", "mis-executive-jobs"),
]

if __name__ == "__main__":
    all_jobs = []

    for search_keyword, url_slug in TARGET_SEARCHES:
        jobs = scrape_naukri_jobs(search_keyword, url_slug, num_pages=5)
        all_jobs.extend(jobs)

    df = pd.DataFrame(all_jobs)
    df.to_csv("data/raw/naukri_jobs.csv", index=False)

    print(f"\nDone. Total jobs scraped: {len(all_jobs)}")
    print("Saved to data/raw/naukri_jobs.csv")
