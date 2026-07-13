from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_naukri_jobs(search_keyword, url_slug, num_pages=5):
    """
    Scrapes Naukri job listings for a given search keyword.

    search_keyword: the human-readable term (e.g. "data analyst") - stored
                     in each job record so we know which search found it
    url_slug: the exact URL-friendly version Naukri uses
              (e.g. "data-analyst-jobs")
    num_pages: how many pages of results to scrape

    Returns a list of job dictionaries.
    """

    options = Options()
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    jobs_for_this_keyword = []

    print(f"Started scraping: {search_keyword}")

    for page_num in range(1, num_pages + 1):
        if page_num == 1:
            url = f"https://www.naukri.com/{url_slug}"
        else:
            url = f"https://www.naukri.com/{url_slug}-{page_num}"

        driver.get(url)
        time.sleep(5)

        print("Page title:", driver.title)

        job_cards = driver.find_elements(By.CLASS_NAME, "cust-job-tuple")

        for card in job_cards:
            title = card.find_element(By.CLASS_NAME, "title").text
            company = card.find_element(By.CLASS_NAME, "comp-name").text

            try:
                experience = card.find_element(By.CLASS_NAME, "expwdth").text
            except:
                experience = "Not Specified"
            try:
                salary = card.find_element(By.CLASS_NAME, "sal").text
            except:
                salary = "Not Specified"
            try:
                location = card.find_element(By.CLASS_NAME, "locWdth").text
            except:
                location = "Not Specified"
            try:
                description = card.find_element(By.CLASS_NAME, "job-desc").text
            except:
                description = "Not Specified"

            posted_day = card.find_element(By.CLASS_NAME, "job-post-day").text

            skill_elements = card.find_elements(By.CLASS_NAME, "tag-li")
            skills = [skill.text for skill in skill_elements]

            job_data = {
                "title": title,
                "company": company,
                "location": location,
                "experience": experience,
                "salary": salary,
                "description": description,
                "posted": posted_day,
                "skills": skills,
                "search_keyword": search_keyword
            }

            jobs_for_this_keyword.append(job_data)

        time.sleep(10)
        print(f"Page {page_num} loaded for '{search_keyword}'")

    driver.quit()
    return jobs_for_this_keyword