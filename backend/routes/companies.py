from fastapi import APIRouter
from database.connection import get_connection

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("/", response_model=list[str])
def list_companies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT company FROM jobs WHERE archived = FALSE ORDER BY company ASC")
    companies = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return companies
