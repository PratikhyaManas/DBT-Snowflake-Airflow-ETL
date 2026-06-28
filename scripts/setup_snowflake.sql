-- Setup script for Snowflake environment
use role sysadmin;

create warehouse if not exists dbt_wh with warehouse_size = 'xsmall';
create database if not exists ecommerce_db;
create schema if not exists ecommerce_db.raw;
create schema if not exists ecommerce_db.analytics;

-- Create role and grants (replace with your user)
create role if not exists dbt_role;
grant role dbt_role to user YOUR_USER;
grant usage on warehouse dbt_wh to role dbt_role;
grant all on database ecommerce_db to role dbt_role;
