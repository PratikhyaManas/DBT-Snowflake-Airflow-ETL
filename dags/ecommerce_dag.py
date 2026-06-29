"""dbt + Snowflake ETL DAG orchestrated by Astronomer Cosmos."""

import os
from datetime import datetime, timedelta
from pathlib import Path
from urllib import request

from cosmos import DbtDag, ExecutionConfig, ProfileConfig, ProjectConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

DBT_PROJECT_PATH = Path(__file__).resolve().parents[1]
SNOWFLAKE_CONN_ID = "snowflake_conn"
DBT_PROFILE_NAME = "ecommerce_dbt"
DBT_TARGET_NAME = "dev"

PROFILE_ARGS = {
    "database": "ecommerce_db",
    "schema": "analytics",
    "warehouse": "dbt_wh",
    "role": "dbt_role",
}

ALERT_WEBHOOK_URL = os.getenv("AIRFLOW_ALERT_WEBHOOK_URL", "")


def notify_failure(context):
    """Send best-effort DAG failure alerts to a webhook (Slack/Teams compatible)."""
    if not ALERT_WEBHOOK_URL:
        return

    dag_id = context.get("dag").dag_id if context.get("dag") else "unknown"
    task_id = context.get("task_instance").task_id if context.get("task_instance") else "unknown"
    run_id = context.get("run_id", "unknown")
    payload = (
        '{"text":"Airflow failure: DAG=' + dag_id + ', task=' + task_id + ', run_id=' + run_id + '"}'
    ).encode("utf-8")

    req = request.Request(
        ALERT_WEBHOOK_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        request.urlopen(req, timeout=10)
    except Exception:
        # Keep alert failures from failing the DAG itself.
        return

profile_config = ProfileConfig(
    profile_name=DBT_PROFILE_NAME,
    target_name=DBT_TARGET_NAME,
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id=SNOWFLAKE_CONN_ID,
        profile_args=PROFILE_ARGS,
    ),
)

ecommerce_dbt_pipeline = DbtDag(
    dag_id="ecommerce_dbt_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "on_failure_callback": notify_failure,
    },
    project_config=ProjectConfig(dbt_project_path=DBT_PROJECT_PATH),
    profile_config=profile_config,
    execution_config=ExecutionConfig(dbt_executable_path="dbt"),
    operator_args={
        "install_deps": True,
        "execution_timeout": timedelta(minutes=30),
    },
)