select
    *,
    SNOWFLAKE.CORTEX.COMPLETE(
        'llama3-8b', 
        'Summarize this order: ' || order_id || ' - Total: ' || total_amount
    ) as order_summary
from {{ ref('fct_sales') }}