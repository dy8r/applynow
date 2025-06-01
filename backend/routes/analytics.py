# analytics.py
from fastapi import APIRouter, Request
from hashlib import sha256
from database.connection import get_connection

router = APIRouter()

@router.post("/analytics")
async def log_analytics(request: Request):
    data = await request.json()
    path = data.get("path")

    # Extract IP & User Agent
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")

    # Hash IP to preserve privacy
    hashed_ip = sha256(ip.encode()).hexdigest()

    # Insert into DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO page_analytics (hashed_ip, path, user_agent)
        VALUES (%s, %s, %s)
    """, (hashed_ip, path, user_agent))
    conn.commit()
    conn.close()

    return {"status": "ok"}
