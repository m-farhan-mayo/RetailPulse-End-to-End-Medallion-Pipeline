from fastapi import APIRouter
from sqlalchemy import text

from app.database import engine

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/top-products")

def top_products():

    query = """

    SELECT *
    FROM silver.top_products

    ORDER BY total_revenue DESC

    """

    with engine.connect() as conn:

        result = conn.execute(text(query))

        rows = result.fetchall()

    return [
        dict(row._mapping)
        for row in rows
    ]