from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# ---------------- DEFAULT ARGS ---------------- #

default_args = {

    "owner": "retailpulse",
    "start_date": datetime(2026, 5, 1),

    "retries": 1
}

# ---------------- DAG ---------------- #

with DAG(

    dag_id="retailpulse_pipeline",

    default_args=default_args,

    schedule="@daily",

    catchup=False

) as dag:

    # ---------------- VALIDATION ---------------- #

    validate_data = BashOperator(

        task_id="validate_data",

        bash_command="""
        cd /opt/airflow &&
        python scripts/validation/run_validation.py
        """
    )

    # ---------------- LOAD POSTGRES ---------------- #

    load_postgres = BashOperator(

        task_id="load_postgres",

        bash_command="""
        cd /opt/airflow &&
        python scripts/load_to_postgres.py
        """
    )

    # ---------------- DBT SILVER ---------------- #

    dbt_silver = BashOperator(

        task_id="dbt_silver",

        bash_command="""
        cd /opt/airflow &&
        dbt run --select silver --project-dir dbt/retailpulse_dbt
        """
    )

    # ---------------- DBT GOLD ---------------- #

    dbt_gold = BashOperator(

        task_id="dbt_gold",

        bash_command="""
        cd /opt/airflow &&
        dbt run --select gold --project-dir dbt/retailpulse_dbt
        """
    )

    # ---------------- EXPORT GOLD ---------------- #

    export_gold = BashOperator(

        task_id="export_gold",

        bash_command="""
        cd /opt/airflow &&
        python ai/scripts/export_gold_data.py
        """
    )

    # ---------------- CHROMA INGEST ---------------- #

    chroma_ingest = BashOperator(

        task_id="chroma_ingest",

        bash_command="""
        cd /opt/airflow &&
        python ai/scripts/ingest_to_chroma.py
        """
    )

    # ---------------- API HEALTH CHECK ---------------- #

    api_healthcheck = BashOperator(

        task_id="api_healthcheck",

        bash_command="""
        curl http://host.docker.internal:8000/health
        """
    )

    # ---------------- PIPELINE FLOW ---------------- #

    validate_data >> load_postgres

    load_postgres >> dbt_silver

    dbt_silver >> dbt_gold

    dbt_gold >> export_gold

    export_gold >> chroma_ingest

    chroma_ingest >> api_healthcheck