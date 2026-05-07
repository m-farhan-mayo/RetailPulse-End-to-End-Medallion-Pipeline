from fastapi import APIRouter
from sqlalchemy import text

from app.database import engine

router = APIRouter(
    prefix="/stores",
    tags=["Stores"]
)

@router.get("/performance")

def store_performance():

    query = """

    SELECT *
    FROM silver.store_performance

    ORDER BY total_revenue DESC

    """

    with engine.connect() as conn:

        result = conn.execute(text(query))

        rows = result.fetchall()

    return [
        dict(row._mapping)
        for row in rows
    ]