from database.connection import get_connection
import json


def build_where_clauses(filters: dict):
    where_clauses = ["archived = FALSE"]
    values = []

    for key, val in filters.items():
        if key == 'is_swe' and val == True:
            if val is not None:
                where_clauses.append("department = %s")
                values.append('software_engineering')
                continue
        if val is None:
            continue
        if isinstance(val, list) and val:
            placeholders = ','.join(['%s'] * len(val))
            where_clauses.append(f"{key} IN ({placeholders})")
            values.extend(val)
        elif isinstance(val, bool):
            where_clauses.append(f"{key} = %s")
            values.append(val)
        elif isinstance(val, (int, float, str)):
            where_clauses.append(f"{key} = %s")
            values.append(val)

    return where_clauses, values

def get_jobs(
    offset=0,
    limit=20,
    company=None,
    title=None,
    location=None,
    job_type=None,
    department=None,
    industry=None,
    work_model=None,
    seniority=None,
    technologies=None,
    is_winnipeg=None,
    salary_min=None,
    salary_max=None,
    min_experience=None,
    is_swe=None
):
    filters = {
        "company": company,
        "title": title,
        "location": location,
        "job_type": job_type,
        "department": department,
        "industry": industry,
        "work_model": work_model,
        "seniority": seniority,
        "is_winnipeg": is_winnipeg,
        "is_swe": is_swe,
    }

    where_clauses, values = build_where_clauses(filters)

    # Numeric filters
    if salary_min is not None:
        where_clauses.append("salary_min >= %s")
        values.append(salary_min)
    if salary_max is not None:
        where_clauses.append("salary_max <= %s")
        values.append(salary_max)
    if min_experience is not None:
        where_clauses.append("min_experience >= %s")
        values.append(min_experience)

    # Technologies filter: match any
    if technologies:
        for tech in technologies:
            where_clauses.append("technologies LIKE %s")
            values.append(f"%{tech}%")

    where_sql = " AND ".join(where_clauses)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Query for paginated results
    query = f"""
        SELECT * FROM jobs
        WHERE {where_sql}
        ORDER BY last_seen DESC
        LIMIT %s OFFSET %s
    """
    cursor.execute(query, values + [limit, offset])
    rows = cursor.fetchall()

    # Query for total count of matching rows (no pagination)
    count_query = f"SELECT COUNT(*) as total FROM jobs WHERE {where_sql}"
    cursor.execute(count_query, values)
    total = cursor.fetchone()["total"]

    # Decode technologies JSON
    for row in rows:
        try:
            row["technologies"] = json.loads(row["technologies"])
        except Exception:
            row["technologies"] = []

    cursor.close()
    conn.close()

    return {
        "data": rows,
        "total": total,
        "page": (offset // limit) + 1,
        "page_size": limit,
    }

def get_job_by_id(job_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        try:
            row["technologies"] = json.loads(row["technologies"])
        except Exception:
            row["technologies"] = []
        return row
    return None
