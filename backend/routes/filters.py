# routes/filters.py

from fastapi import APIRouter
from database.connection import get_connection

router = APIRouter()

@router.get("/filters")
def get_filter_options():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT seniority, job_type, work_model, department, industry
        FROM jobs
        WHERE archived = FALSE
    """)
    rows = cursor.fetchall()

    def count_options(field, normalize=lambda x: x):
        values = [normalize(row[field]) for row in rows if row[field]]
        unique = set(values)
        return [
            {
                "id": value,
                "label": value.replace("-", " ").replace("_", " ").title(),
                "count": values.count(value),
            }
            for value in unique
        ]

    return {
        "seniority": sorted(count_options("seniority", lambda x: x.lower()), key=lambda x: -x["count"]),
        "jobTypes": sorted(count_options("job_type", lambda x: x.lower().replace(" ", "-")), key=lambda x: -x["count"]),
        "workModels": sorted(count_options("work_model", lambda x: x.lower()), key=lambda x: -x["count"]),
        "departments": sorted(count_options("department", lambda x: x.lower().replace(" ", "_")), key=lambda x: -x["count"]),
        "industries": sorted(count_options("industry", lambda x: x.lower().replace(" ", "-")), key=lambda x: -x["count"]),
    }
