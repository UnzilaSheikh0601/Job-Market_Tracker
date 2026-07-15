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
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    jobs_for_this_keyword = []
    prev_page_urls = set()          

    print(f"Started scraping: {search_keyword}")

    for page_num in range(1, num_pages + 1):
        if page_num == 1:
            url = f"https://www.naukri.com/{url_slug}"
        else:
            url = f"https://www.naukri.com/{url_slug}-{page_num}"

        max_retries = 2
        for attempt in range(max_retries + 1):
            driver.get(url)
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cust-job-tuple"))
                )
                break  # succeeded, exit retry loop
            except:
                if attempt < max_retries:
                    print(f"Timed out on page {page_num}, retrying (attempt {attempt + 2})...")
                    time.sleep(5)
                else:
                    print(f"Failed to load page {page_num} after {max_retries + 1} attempts.")

        print("Page title:", driver.title)

        job_cards = driver.find_elements(By.CLASS_NAME, "cust-job-tuple")

        if not job_cards:
            print(f"No job cards found on page {page_num}, stopping.")
            break
        
        jobs_before_this_page = len(jobs_for_this_keyword)

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
                posted_duration = card.find_element(By.CLASS_NAME, "job-post-day").text
            except:
                posted_duration = "Not Specified"
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
                "posted_duration": posted_duration,
                "skills": skills,
                "job_url": job_url,
                "search_keyword": search_keyword
            }
            if title == "Not Specified":
                continue 

            jobs_for_this_keyword.append(job_data)

        jobs_added_this_page = jobs_for_this_keyword[jobs_before_this_page:]
        current_urls = {j["job_url"] for j in jobs_added_this_page}
        
        if current_urls and current_urls == prev_page_urls:
            print(f"No new jobs on page {page_num}, stopping early.")
            break
        prev_page_urls = current_urls

        time.sleep(10)
        print(f"Page {page_num} loaded for '{search_keyword}'")

    driver.quit()
    return jobs_for_this_keyword