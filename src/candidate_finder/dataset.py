from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "knowledge-base"
print(OUTPUT_DIR)
OUTPUT_DIR.mkdir(exist_ok=True)

NUM_CVS = 20

roles = [
    "Java Backend Engineer",
    "Engineering Manager",
    "Python Developer",
    "Data Engineer",
    "DevOps Engineer",
    "Frontend Engineer",
    "AI Engineer",
]


def generate_cv(index: int) -> str:
    role = roles[index % len(roles)]

    prompt = f"""
Generate a realistic but completely fictional CV for a candidate.

Target role: {role}

Requirements:
- Candidate must be fictional
- Do not use real people
- 3 to 15 years of experience
- Include name, summary, skills, work experience, education
- Include realistic technologies and achievements
- Vary seniority and skill level
- Some candidates should have skill gaps
- Keep the CV around 500-800 words
- Return Markdown only

Format:

# Candidate Name

## Summary

## Skills

## Experience

### Company - Role
Dates

- Achievement
- Achievement

## Education
"""

    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
    )

    return response.output_text


for i in range(NUM_CVS):
    cv = generate_cv(i)

    file_path = OUTPUT_DIR / f"candidate_{i + 1:03}.md"
    file_path.write_text(cv, encoding="utf-8")

    print(f"Created {file_path}")

print("Dataset generation complete.")