import pandas as pd
from sqlalchemy import create_engine

# ---------------- POSTGRES ---------------- #

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/retailpulse"
)

# ---------------- EXPORT TABLES ---------------- #

tables = [
    "monthly_sales_by_store",
    "top_products",
    "store_performance",
    "revenue_summary"
]

for table in tables:

    query = f"SELECT * FROM silver.{table}"

    df = pd.read_sql(query, engine)

    output_path = f"ai/data/exports/{table}.csv"

    df.to_csv(output_path, index=False)

    print(f"✅ Exported {table}")