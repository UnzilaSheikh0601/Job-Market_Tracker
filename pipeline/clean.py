import pandas as pd
import ast
import re

SKILL_NORMALIZATION_MAP = {
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "bi": "Power BI",
 
    "python": "Python",
    "python programming": "Python",
    "python scripting": "Python",
    "python data": "Python",
    "python data analytics": "Python",
 
    "sql": "SQL",
 
    "data analytics": "Data Analytics",
    "data analysis": "Data Analytics",
 
    "tableau": "Tableau",
    "excel": "Excel",
    "advanced excel": "Excel",
    "ms office": "MS Office",
 
    "machine learning": "Machine Learning",
    "artificial intelligence": "Artificial Intelligence",
}

def normalize_skill(raw_skill):
    key = raw_skill.strip().lower()

    if key in SKILL_NORMALIZATION_MAP:
        return SKILL_NORMALIZATION_MAP[key]
    
    return raw_skill.strip().title()

def normalize_skill_list(raw_skills):
    cleaned = [normalize_skill(skill) for skill in raw_skills]

    seen = set()
    deduplicated = []
    for skill in cleaned:
        if skill not in seen:
            deduplicated.append(skill)
            seen.add(skill)

    return deduplicated

def parse_experience(text):
    if not isinstance(text, str):
        return (None, None)
    
    text_lower = text.lower()
    match = re.search(r'(\d+)\s*-\s*(\d+)\s*yrs', text_lower)
    if match:
        return (int(match.group(1)), int(match.group(2)))
    
    single_match = re.search(r'(\d+)\s*yrs', text_lower)
    if single_match:
        value = int(single_match.group(1))
        return (value, value)
    
    return (None, None)

def parse_salary(text):
    if not isinstance(text, str):
        return(None, None)

    text_lower = text.lower()

    if 'not specified' in text_lower or 'unpaid' in text_lower:
        return(None, None)

    cleaned = text.replace(",", '')

    match = re.search(r"([\d.]+)\s*-\s*([\d.]+)", cleaned)
    if not match:
        return (None, None)
    
    min_val = float(match.group(1))
    max_val = float(match.group(2))

    if 'lac' in text_lower:
        if min_val < 1000:
            min_val *= 100000
        if max_val < 1000:
            max_val *= 100000

    return (int(min_val), int(max_val))

def clean_jobs_csv(input_path, output_path):
    df = pd.read_csv(input_path)

    df["skills"] = df["skills"].apply(ast.literal_eval)

    df["skills"] = df["skills"].apply(normalize_skill_list)

    df["min_salary"], df["max_salary"] = zip(*df['salary'].apply(parse_salary))

    df["min_experience"], df["max_experience"] = zip(*df['experience'].apply(parse_experience))

    df[['title', 'company', 'location', 'experience', 'min_experience', 'max_experience', 'salary', 'min_salary', 'max_salary', 'description', 'skills', 'posted_duration', 'job_url', 'search_keyword']].to_csv(output_path, index=False)


    print(f"Cleaned {len(df)} rows.")
    print(f"Saved to {output_path}")

    return df