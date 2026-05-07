import os
import yaml
import pandas as pd
from dotenv import load_dotenv
from adlfs import AzureBlobFileSystem

# ================= LOAD ENV ================= #
load_dotenv()

with open("configs/pipeline.yaml", "r") as f:
    config = yaml.safe_load(f)

account_name = os.getenv(config["storage"]["account_name_env"])
account_key = os.getenv(config["storage"]["account_key_env"])

rules = config["rules"]

storage_options = {
    "account_name": account_name,
    "account_key": account_key
}

# ================= ADLS FS ================= #
fs = AzureBlobFileSystem(
    account_name=account_name,
    account_key=account_key
)

# ================= BASE PATHS ================= #
BRONZE = f"abfs://bronze@{account_name}.dfs.core.windows.net/retailpulse"
CLEAN = f"abfs://clean@{account_name}.dfs.core.windows.net/retailpulse"
QUARANTINE = f"abfs://quarantine@{account_name}.dfs.core.windows.net/retailpulse"


# ================= SAFE WRITER ================= #
def write_parquet(df, path, filename):
    full_path = f"{path}/{filename}.parquet"

    df.to_parquet(
        full_path,
        engine="pyarrow",
        index=False,
        storage_options=storage_options
    )


# ================= SAFE JSON READER ================= #
def read_json_folder(path):

    try:
        files = fs.ls(path)
    except Exception:
        return pd.DataFrame()

    all_data = []

    for f in files:
        if f.endswith(".json"):
            df = pd.read_json(
                f"abfs://{f}",
                storage_options=storage_options
            )
            all_data.append(df)

    if not all_data:
        return pd.DataFrame()

    return pd.concat(all_data, ignore_index=True)


# =========================================================
# SALES
# =========================================================
def process_sales():

    print("\n🔵 SALES PROCESSING...")

    df = pd.read_parquet(
        f"{BRONZE}/sales/",
        storage_options=storage_options
    )

    original = len(df)

    df = df.drop_duplicates(subset=["order_id"])

    df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    valid = df[
        (df["qty"] >= rules["qty_min"]) &
        (df["price"] >= rules["price_min"]) &
        (~df["date"].isna())
    ]

    invalid = df[~df.index.isin(valid.index)]

    for d in [valid, invalid]:
        d["year"] = d["date"].dt.year.astype(str)
        d["month"] = d["date"].dt.month.astype(str).str.zfill(2)
        d["day"] = d["date"].dt.day.astype(str).str.zfill(2)

    write_parquet(valid, f"{CLEAN}/sales", "sales_clean")
    write_parquet(invalid, f"{QUARANTINE}/sales", "sales_quarantine")

    print({"sales_original": original, "sales_valid": len(valid), "sales_invalid": len(invalid)})


# =========================================================
# PRODUCTS
# =========================================================
def process_products():

    print("\n🟡 PRODUCTS PROCESSING...")

    df = read_json_folder(f"{BRONZE}/products/")

    if df.empty:
        print("No product data found")
        return

    original = len(df)

    df = df.drop_duplicates(subset=["id"])

    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    valid = df[df["price"].notna()]
    invalid = df[df["price"].isna()]

    write_parquet(valid, f"{CLEAN}/products", "products_clean")
    write_parquet(invalid, f"{QUARANTINE}/products", "products_quarantine")

    print({"products_original": original, "products_valid": len(valid), "products_invalid": len(invalid)})


# =========================================================
# CURRENCY
# =========================================================
def process_currency():

    print("\n🟢 CURRENCY PROCESSING...")

    df = read_json_folder(f"{BRONZE}/currency/")

    if df.empty:
        print("No currency data found")
        return

    original = len(df)

    valid = df[df["base_code"].notna()]
    invalid = df[df["base_code"].isna()]

    write_parquet(valid, f"{CLEAN}/currency", "currency_clean")
    write_parquet(invalid, f"{QUARANTINE}/currency", "currency_quarantine")

    print({"currency_original": original, "currency_valid": len(valid), "currency_invalid": len(invalid)})


# =========================================================
# MAIN RUNNER
# =========================================================
def run():

    print("\n🚀 STARTING PIPELINE...\n")

    try:
        process_sales()
        process_products()
        process_currency()

    except Exception as e:
        import traceback
        traceback.print_exc()

    print("\n🎯 PIPELINE COMPLETED\n")


if __name__ == "__main__":
    run()