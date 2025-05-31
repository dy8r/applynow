import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import mysql.connector

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
