import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import TypedDict, Literal, Optional, List
import os


load_dotenv()

class JobEnrichment(TypedDict):
    salary_min: Optional[int]
    salary_max: Optional[int]
    work_model: Optional[Literal["remote", "on-site", "hybrid"]]
    industry: Optional[str]
    seniority: Optional[Literal["entry", "mid", "senior", "lead"]]
    technologies: List[str]
    is_winnipeg: bool
    department: Optional[
        Literal[
            "software_engineering",
            "management",
            "design",
            "marketing",
            "sales",
            "hr",
            "finance",
            "support",
            "operations",
            "other"
        ]
    ]
    min_experience: Optional[int]


api_key = os.getenv("OPENAI_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_KEY in .env")
client = OpenAI(api_key=api_key)


def enrich_job_posting(job_post_text: str) -> JobEnrichment:
    prompt = f"""
You are an AI that extracts structured information from job postings.
Below is a job post (may be in HTML or plain text):

---
{job_post_text}
---

Extract and return this exact JSON object:

{{
  "salary_min": integer or null,
  "salary_max": integer or null,
  "work_model": one of ["remote", "on-site", "hybrid", null],
  "industry": string or null,
  "seniority": one of ["entry", "mid", "senior", "lead", null],
  "technologies": list of strings,
  "is_winnipeg": boolean,
  "department": one of [
    "software_engineering",
    "management",
    "design",
    "marketing",
    "sales",
    "hr",
    "finance",
    "support",
    "operations",
    "other"
  ],
  "min_experience": integer or null  // number of years of experience required (e.g., 3)
}}

Instructions:
- Use `is_winnipeg = true` if the job is clearly located in Winnipeg, MB or Manitoba. Any other city or province should set it to `false`.
- Choose the most appropriate `department`, based on title and content.
- If a field is not explicitly stated or inferable, use `null` or an empty list.
- Return only valid JSON, nothing else.
"""

    default: JobEnrichment = {
        "salary_min": None,
        "salary_max": None,
        "work_model": None,
        "industry": None,
        "seniority": None,
        "technologies": [],
        "is_winnipeg": False,
        "department": None,
        "min_experience": None,
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        content = response.choices[0].message.content
        result = json.loads(content)

        # Fill missing fields with default values
        for key in default:
            if key not in result or result[key] is None:
                result[key] = default[key]
            elif key == "technologies" and not isinstance(result[key], list):
                result[key] = []

        return result  # type: ignore

    except Exception as e:
        print(f"⚠️ OpenAI API call failed or returned invalid JSON: {e}")
        return default
