from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    prev_page_urls = set()          

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

        if not job_cards:
            print(f"No job cards found on page {page_num}, stopping.")
            break

        for card in job_cards:
            try:
                title_element = card.find_element(By.CLASS_NAME, "title")
                title = title_element.text
                job_url = title_element.get_attribute("href")
            except:
                title = "Not Specified"
                job_url = None
            try:
                company = card.find_element(By.CLASS_NAME, "comp-name").text
            except:
                company = "Not Specified"        
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
            try:
                posted_day = card.find_element(By.CLASS_NAME, "job-post-day").text
            except:
                posted_day = "Not Specified"
            try:
                skill_elements = card.find_elements(By.CLASS_NAME, "tag-li")
                skills = [skill.text for skill in skill_elements]
            except:
                skills = []

            job_data = {
                "title": title,
                "company": company,
                "location": location,
                "experience": experience,
                "salary": salary,
                "description": description,
                "posted": posted_day,
                "skills": skills,
                "job_url": job_url,
                "search_keyword": search_keyword
            }

            jobs_for_this_keyword.append(job_data)

        current_urls = {j["job_url"] for j in jobs_for_this_keyword[-len(job_cards):]}
        if current_urls and current_urls == prev_page_urls:
            print(f"No new jobs on page {page_num}, stopping early.")
            break
        prev_page_urls = current_urls

        time.sleep(10)
        print(f"Page {page_num} loaded for '{search_keyword}'")

    driver.quit()
    return jobs_for_this_keyword