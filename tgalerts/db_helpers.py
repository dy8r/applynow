import os
import json
import mysql.connector
from typing import List
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

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


def get_pending_job_notifications() -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM job_notifications_queue
        WHERE notified = FALSE AND event_type = 'new'
        ORDER BY created_at ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def mark_notifications_sent(job_ids: List[str]):
    if not job_ids:
        return

    conn = get_connection()
    cursor = conn.cursor()
    format_strings = ','.join(['%s'] * len(job_ids))
    cursor.execute(f"""
        UPDATE job_notifications_queue
        SET notified = TRUE
        WHERE job_id IN ({format_strings})
    """, tuple(job_ids))
    conn.commit()
    conn.close()


def get_job_by_id(job_id: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM jobs
        WHERE id = %s
    """, (job_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_active_users_with_alerts() -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            u.id AS user_id,
            u.username,
            f.*
        FROM users u
        INNER JOIN job_alert_filters f ON u.id = f.user_id
        WHERE f.is_active = TRUE
        ORDER BY f.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
