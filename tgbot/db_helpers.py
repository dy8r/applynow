from typing import Optional, List
import mysql.connector
import json
import os
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

def create_user(user_id: int, username: Optional[str]):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        INSERT INTO users (id, username)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE username = VALUES(username)
    """, (user_id, username))
    conn.commit()

def create_default_alert_if_not_exists(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id FROM job_alert_filters
        WHERE user_id = %s
    """, (user_id,))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute("""
            INSERT INTO job_alert_filters (user_id, is_winnipeg)
            VALUES (%s, TRUE)
        """, (user_id,))
        conn.commit()
    
    conn.close()

def get_user_alert_settings(user_id: int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM job_alert_filters
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id,))
    return cursor.fetchone()

def toggle_json_field(user_id: int, field: str, value: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"""
        SELECT id, {field} FROM job_alert_filters
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id,))
    row = cursor.fetchone()
    if not row:
        return False

    current_values = json.loads(row[field]) if row[field] else []
    if value in current_values:
        current_values.remove(value)
    else:
        current_values.append(value)

    cursor.execute(f"""
        UPDATE job_alert_filters
        SET {field} = %s
        WHERE id = %s
    """, (json.dumps(current_values), row["id"]))
    conn.commit()
    return True

def get_filter_field(user_id: int, field: str) -> List[str]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"""
        SELECT {field} FROM job_alert_filters
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id,))
    row = cursor.fetchone()
    return json.loads(row[field]) if row and row[field] else []

def get_distinct_companies() -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT company FROM jobs WHERE archived = FALSE")
    return sorted([row[0] for row in cursor.fetchall()])

def get_distinct_work_models() -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT work_model FROM jobs WHERE archived = FALSE")
    return sorted([row[0] for row in cursor.fetchall() if row[0]])

def get_distinct_seniorities() -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT seniority FROM jobs WHERE archived = FALSE")
    return sorted([row[0] for row in cursor.fetchall() if row[0]])

def get_distinct_departments() -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT department FROM jobs WHERE archived = FALSE")
    return sorted([row[0] for row in cursor.fetchall() if row[0]])

def toggle_boolean_field(user_id: int, field: str) -> bool:
    """
    Toggle a boolean field like 'is_winnipeg' or 'is_active' for the user's active alert.
    Returns the new value.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"""
        SELECT id, {field}
        FROM job_alert_filters
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id,))
    row = cursor.fetchone()
    if not row:
        return False

    new_value = not bool(row[field])
    cursor.execute(f"""
        UPDATE job_alert_filters
        SET {field} = %s
        WHERE id = %s
    """, (new_value, row["id"]))
    conn.commit()
    conn.close()
    return new_value

def get_alert_status_flags(user_id: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT is_active, is_winnipeg
        FROM job_alert_filters
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id,))
    row = cursor.fetchone()
    return row if row else {"is_active": True, "is_winnipeg": True}
