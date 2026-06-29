# Modern ETL with Snowflake, dbt, and Airflow (Cosmos)

This repository implements a practical modern ETL/ELT workflow:

1. Source data from Snowflake sample dataset (`snowflake_sample_data.tpch_sf1`)
2. Transform with dbt in layered models (`staging -> intermediate -> marts`)
3. Validate with dbt tests and Great Expectations
4. Orchestrate the dbt pipeline in Airflow using Astronomer Cosmos

## Repository Structure

- `models/staging/`
  - source declarations and thin cleanup models
- `models/marts/intermediate/`
  - reusable joins and business prep models
- `models/marts/`
  - final fact model and semantic model config
- `macros/`
  - reusable dbt SQL macro (`discounted_amount`)
- `tests/`
  - singular dbt tests
- `dags/`
  - Airflow DAG powered by Cosmos
- `scripts/`
  - Snowflake bootstrap SQL
- `great_expectations/`
  - additional data quality checks

## Prerequisites

- Python 3.10+
- Snowflake account
- Airflow environment (local Airflow or Astro runtime)

## Snowflake Setup

Execute:

```sql
-- run in Snowflake worksheet
-- file: scripts/setup_snowflake.sql
```

Update `YOUR_USER` in `scripts/setup_snowflake.sql` before running.

## dbt Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your dbt profile (`~/.dbt/profiles.yml`):

```yaml
ecommerce_dbt:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: <snowflake_account>
      user: <snowflake_user>
      password: <snowflake_password>
      role: dbt_role
      warehouse: dbt_wh
      database: ecommerce_db
      schema: analytics
      threads: 4
```

Install dbt packages and run:

```bash
dbt deps
dbt build
```

Run source freshness checks:

```bash
dbt source freshness
```

`fct_sales` is configured as an incremental model (merge strategy). Use a full refresh when needed:

```bash
dbt run --select fct_sales --full-refresh
```

## Airflow + Cosmos Orchestration

The DAG in `dags/ecommerce_dag.py` creates a native model-aware dbt DAG.

Requirements:

- Airflow connection named `snowflake_conn`
- Python packages from `requirements.txt`

Run in Airflow:

1. Configure `snowflake_conn` in Airflow UI
2. Start scheduler/webserver
3. Trigger DAG: `ecommerce_dbt_pipeline`

Optional alerting:

- Set env var `AIRFLOW_ALERT_WEBHOOK_URL` in Airflow to receive DAG failure alerts (Slack/Teams compatible webhook).

## Data Quality

This project uses:

- dbt generic tests in `models/marts/generic_tests.yml`
- dbt singular test in `tests/fct_sales_discount.sql`
- Great Expectations suite in `great_expectations/expectations/orders_suite.json`

Data contracts and stronger schema tests are enabled for `fct_sales`:

- model contract enforcement (`contract.enforced: true`)
- explicit column data types and not-null constraints
- domain/value checks (`accepted_values`, `accepted_range`)
- business-rule assertion for net sales formula

Equivalent staging contracts/tests are enabled for:

- `stg_orders`
- `stg_order_items`

Staging contract/test definitions are in `models/staging/staging_tests.yml`.

Run contract-aware validation:

```bash
dbt build --select stg_orders stg_order_items
dbt build --select fct_sales
dbt test --select stg_orders stg_order_items
dbt test --select fct_sales
```

## CI/CD

The pipeline is split for cleaner governance and easier troubleshooting:

- `.github/workflows/sast.yml`: `CodeQL`, `Bandit`
- `.github/workflows/ci.yml`: `Dependency Audit`, `dbt Validate`
- `.github/workflows/cd.yml`: `Deploy dbt + GE` (runs only for successful `main` workflow runs)

CD is triggered via `workflow_run` and only deploys when the triggering run is:

- successful (`conclusion == success`)
- for branch `main`

### Required GitHub Secrets for CD

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_ROLE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`

### Branch Protection Recommendations (`main`)

In GitHub branch protection for `main`, enable:

1. `Require a pull request before merging`
2. `Require status checks to pass before merging`
3. `Require branches to be up to date before merging`

Set these required status checks:

1. `CodeQL`
2. `Bandit`
3. `Dependency Audit`
4. `dbt Validate`

Optional hardening:

1. `Require conversation resolution before merging`
2. `Require signed commits`
3. `Do not allow bypassing the above settings`
