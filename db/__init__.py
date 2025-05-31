import os
import mysql.connector
from dotenv import load_dotenv

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def apply_schema():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set in .env")

    # Parse MySQL connection info
    import urllib.parse as urlparse
    parsed = urlparse.urlparse(db_url)

    config = {
        'host': parsed.hostname,
        'port': parsed.port or 3306,
        'user': parsed.username,
        'password': parsed.password,
        'database': parsed.path.lstrip('/'),
    }

    try:
        print("🔌 Connecting to MySQL...")
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        print("📄 Applying schema...")
        with open(SCHEMA_PATH, "r") as f:
            schema_sql = f.read()
            for statement in schema_sql.split(";"):
                if statement.strip():
                    cursor.execute(statement)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Schema applied successfully.")

    except Exception as e:
        print(f"❌ Failed to apply schema: {e}")

if __name__ == "__main__":
    apply_schema()
