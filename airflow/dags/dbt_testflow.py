from pendulum import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from cosmos.providers.dbt.task_group import DbtTaskGroup

from cosmos.providers.dbt import DbtSeedOperator


with DAG(
    dag_id="extract_dag",
    start_date=datetime(2023, 1, 9),
    schedule="@daily",
) as dag:

    e1 = EmptyOperator(task_id="ingestion_workflow")

    seed = DbtSeedOperator(
        task_id="seed",
        project_dir="/dbt/jaffle_shop",
        full_refresh=True,
        conn_id="trino-conn",
        schema="public",
    )

    dbt_tg = DbtTaskGroup(
        group_id="dbt_tg",
        dbt_project_name="",
        dbt_root_path="/dbt/jaffle_shop",
        dbt_models_dir="/dbt/jaffle_shop/models",
        conn_id="dbt_conn",
        dbt_args={"schema": "public"},
    )

    e2 = EmptyOperator(task_id="some_extraction")

    e1 >> seed >> dbt_tg >> e2
