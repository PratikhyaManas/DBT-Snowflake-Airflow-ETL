"""dbt + Snowflake ETL DAG orchestrated by Astronomer Cosmos."""

from datetime import datetime
from pathlib import Path

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
    project_config=ProjectConfig(dbt_project_path=DBT_PROJECT_PATH),
    profile_config=profile_config,
    execution_config=ExecutionConfig(dbt_executable_path="dbt"),
    operator_args={"install_deps": True},
)