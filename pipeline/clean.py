import pandas as pd
import ast

SKILL_NORMALIZATION_MAP = {
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "bi": "Power BI",  # "Bi" alone, seen in your data, is Naukri truncating "Power BI"
 
    "python": "Python",
    "python programming": "Python",
    "python scripting": "Python",
    "python data": "Python",
    "python data analytics": "Python",
 
    "sql": "SQL",
 
    "data analytics": "Data Analytics",
    "data analysis": "Data Analytics",  # merged per project decision
 
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

def clean_jobs_csv(input_path, output_path):
    df = pd.read_csv(input_path)

    df["skills"] = df["skills"].apply(ast.literal_eval)

    df["skills"] = df["skills"].apply(normalize_skill_list)

    df.to_csv(output_path, index=False)
    print(f"Cleaned {len(df)} rows.")
    print(f"Saved to {output_path}")

    return df