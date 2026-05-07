from fastapi import APIRouter
from sqlalchemy import text

from app.database import engine

router = APIRouter(
    prefix="/revenue",
    tags=["Revenue"]
)

# ---------------- KPI SUMMARY ---------------- #

@router.get("/summary")

def revenue_summary():

    query = """

    SELECT *
    FROM silver.revenue_summary

    """

    with engine.connect() as conn:

        result = conn.execute(text(query))

        rows = result.fetchall()

    return [
        dict(row._mapping)
        for row in rows
    ]

# ---------------- MONTHLY SALES ---------------- #

@router.get("/monthly-sales")

def monthly_sales():

    query = """

    SELECT *
    FROM silver.monthly_sales_by_store

    ORDER BY year, month

    """

    with engine.connect() as conn:

        result = conn.execute(text(query))

        rows = result.fetchall()

    return [
        dict(row._mapping)
        for row in rows
    ]