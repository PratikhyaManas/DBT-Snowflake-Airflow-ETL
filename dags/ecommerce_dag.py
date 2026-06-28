from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG('ecommerce_dbt_pipeline', start_date=datetime(2026,1,1))

dbt_run = BashOperator(
    task_id='dbt_build',
    bash_command='cd /path/to/project && dbt build',
    dag=dag
)