import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from adlfs import AzureBlobFileSystem

# ---------------- LOAD ENV ---------------- #

load_dotenv()

# ---------------- STORAGE CONFIG ---------------- #

account_name = os.getenv("AZURE_STORAGE_ACCOUNT")
account_key = os.getenv("AZURE_STORAGE_KEY")

# ---------------- ADLS CONFIG ---------------- #

container = "clean"
base_path = "retailpulse/sales"

fs = AzureBlobFileSystem(
    account_name=account_name,
    account_key=account_key
)

# ---------------- POSTGRES CONFIG ---------------- #

postgres_user = "postgres"
postgres_password = "postgres"
postgres_host = "localhost"
postgres_port = "5432"
postgres_db = "retailpulse"

# ---------------- GET ALL PARQUET FILES ---------------- #

print("\nListing parquet files from ADLS...\n")

all_paths = fs.find(f"{container}/{base_path}")

parquet_files = [f for f in all_paths if f.endswith(".parquet")]

if not parquet_files:
    print("❌ No parquet files found.")
    exit()

print(f"✅ Found {len(parquet_files)} parquet files.\n")

# ---------------- READ FILES ONE BY ONE ---------------- #

dfs = []

for file in parquet_files:

    print(f"Reading: {file}")

    try:
        df = pd.read_parquet(
            f"abfs://{file}",
            storage_options={
                "account_name": account_name,
                "account_key": account_key
            }
        )

        # Drop partition columns if they exist
        for col in ["year", "month", "day"]:
            if col in df.columns:
                df = df.drop(columns=[col])

        dfs.append(df)

    except Exception as e:
        print(f"❌ Failed reading {file}: {e}")

# ---------------- COMBINE DATA ---------------- #

final_df = pd.concat(dfs, ignore_index=True)

print("\n✅ Combined Data Successfully\n")

print(final_df.head())

# ---------------- POSTGRES CONNECTION ---------------- #

engine = create_engine(
    f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
)

# ---------------- LOAD TO POSTGRES ---------------- #

print("\nLoading into PostgreSQL...\n")

final_df.to_sql(
    "sales_clean",
    engine,
    schema="public",
    if_exists="replace",
    index=False
)

print("\n✅ sales_clean table created successfully.\n")