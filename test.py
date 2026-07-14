# from pipeline.clean import normalize_skill_list

# test_skills = ["Power BI", "Power Bi", "PowerBI", "python", "PYTHON PROGRAMMING", "Sql", "Data Analysis", "data analytics"]
# print(normalize_skill_list(test_skills))

from pipeline.clean import clean_jobs_csv

clean_jobs_csv("data/raw/naukri_jobs.csv", "data/processed/naukri_jobs_cleaned.csv")