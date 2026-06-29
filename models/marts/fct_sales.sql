{{
    config(
        materialized='incremental',
        unique_key='order_key',
        incremental_strategy='merge',
        on_schema_change='sync_all_columns'
    )
}}

select
    orders.order_key,
    orders.customer_key,
    orders.order_date,
    orders.status_code,
    orders.total_price,
    item_summary.gross_item_sales_amount,
    item_summary.item_discount_amount,
    (item_summary.gross_item_sales_amount + item_summary.item_discount_amount) as net_item_sales_amount
from {{ ref('stg_orders') }} as orders
join {{ ref('int_order_items_summary') }} as item_summary
    on orders.order_key = item_summary.order_key

{% if is_incremental() %}
where orders.order_date > (select coalesce(max(order_date), '1900-01-01'::date) from {{ this }})
{% endif %}
