# E-commerce Analytics dbt Project with Snowflake CI/CD

Modern DataOps example using dbt + Snowflake + GitHub Actions.

## Project Structure
- `models/staging/` - Raw data cleaning
- `models/marts/` - Transformed business models
- `.github/workflows/` - CI/CD pipelines

## Setup
1. Run `scripts/setup_snowflake.sql`
2. Configure `profiles.yml` with Snowflake credentials
3. `dbt deps`
4. `dbt build`

## CI/CD
- PRs trigger tests (CI)
- Merges to main trigger deployment (CD)
