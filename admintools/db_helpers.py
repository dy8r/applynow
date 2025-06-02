import os
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DB_URL)

def get_distinct_ips(days: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    since = datetime.utcnow() - timedelta(days=days)
    cur.execute(
        "SELECT COUNT(DISTINCT hashed_ip) FROM analytics WHERE timestamp > %s",
        (since,)
    )
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

def get_tg_user_count() -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE tg_id IS NOT NULL")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

def get_enabled_alerts_count() -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM job_alert_filters WHERE is_active = true")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

