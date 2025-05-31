import os
import uuid
import json
import mysql.connector
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# Parse connection
from urllib.parse import urlparse

parsed = urlparse(os.getenv("DATABASE_URL"))
DB_CONFIG = {
    'host': parsed.hostname,
    'port': parsed.port or 3306,
    'user': parsed.username,
    'password': parsed.password,
    'database': parsed.path.lstrip('/')
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def insert_job(job: dict):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO jobs (
        id, company, title, location, job_type, description_html, link,
        salary_min, salary_max, work_model, industry, seniority,
        technologies, is_winnipeg, department, min_experience,
        archived, last_seen
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        FALSE, NOW()
    )
    ON DUPLICATE KEY UPDATE
        title=VALUES(title),
        location=VALUES(location),
        job_type=VALUES(job_type),
        description_html=VALUES(description_html),
        salary_min=VALUES(salary_min),
        salary_max=VALUES(salary_max),
        work_model=VALUES(work_model),
        industry=VALUES(industry),
        seniority=VALUES(seniority),
        technologies=VALUES(technologies),
        is_winnipeg=VALUES(is_winnipeg),
        department=VALUES(department),
        min_experience=VALUES(min_experience),
        archived=FALSE,
        last_seen=NOW();
    """

    cursor.execute(sql, (
        job.get("id", str(uuid.uuid4())),
        job["company"],
        job["title"],
        job.get("location"),
        job.get("job_type"),
        job.get("description_html"),
        job["link"],
        job.get("salary_min"),
        job.get("salary_max"),
        job.get("work_model"),
        job.get("industry"),
        job.get("seniority"),
        json.dumps(job.get("technologies", [])),
        job.get("is_winnipeg", False),
        job.get("department"),
        job.get("min_experience"),
    ))

    conn.commit()
    cursor.close()
    conn.close()


def does_job_exist(link: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM jobs WHERE link = %s LIMIT 1", (link,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None


def update_last_seen(link: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET last_seen = NOW(), archived = FALSE WHERE link = %s", (link,))
    conn.commit()
    cursor.close()
    conn.close()


def archive_missing_jobs(company: str, active_links: list[str]):
    """Mark jobs from this company as archived if their link is not in the latest crawl."""
    conn = get_connection()
    cursor = conn.cursor()
    format_strings = ','.join(['%s'] * len(active_links)) if active_links else "'-no-links-'"
    query = f"""
        UPDATE jobs
        SET archived = TRUE
        WHERE company = %s
        AND (link NOT IN ({format_strings}))
    """
    cursor.execute(query, [company] + active_links)
    conn.commit()
    cursor.close()
    conn.close()


def get_all_links_by_company(company: str) -> list[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT link FROM jobs WHERE company = %s", (company,))
    links = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return links

def insert_job_notification(job_id: str, event_type: str = "new"):
    """Insert a new notification into the queue if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Prevent duplicate event_type per job_id
    cursor.execute("""
        SELECT 1 FROM job_notifications_queue 
        WHERE job_id = %s AND event_type = %s AND notified = FALSE
        LIMIT 1
    """, (job_id, event_type))
    
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO job_notifications_queue (job_id, event_type)
            VALUES (%s, %s)
        """, (job_id, event_type))
        conn.commit()
    
    cursor.close()
    conn.close()


def insert_notification_if_new(link: str):
    """Check if job is new and insert a 'new' notification if it is."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, last_seen FROM jobs WHERE link = %s", (link,))
    row = cursor.fetchone()

    if row:
        job_id, last_seen = row
        # If job is new or just added this run, notify
        insert_job_notification(job_id, "new")

    cursor.close()
    conn.close()


def insert_notification_for_archived(link: str):
    """Insert an 'archived' notification for a job that was marked archived."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM jobs WHERE link = %s AND archived = TRUE", (link,))
    row = cursor.fetchone()

    if row:
        insert_job_notification(row[0], "archived")

    cursor.close()
    conn.close()

def insert_job_notification_by_link(link: str, event_type: str = "new"):
    """Insert a job notification for a given job link."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jobs WHERE link = %s", (link,))
    row = cursor.fetchone()
    if row:
        insert_job_notification(row[0], event_type)
    cursor.close()
    conn.close()