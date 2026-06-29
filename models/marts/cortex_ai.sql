select
    *,
    SNOWFLAKE.CORTEX.COMPLETE(
        'llama3-8b',
        'Summarize this order: ' || order_key || ' - Net Total: ' || net_item_sales_amount
    ) as order_summary
from {{ ref('fct_sales') }}