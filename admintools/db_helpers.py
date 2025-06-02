import os
import mysql.connector
from datetime import datetime, timedelta
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

