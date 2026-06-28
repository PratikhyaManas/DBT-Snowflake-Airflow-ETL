select
    order_id,
    customer_id,
    order_date,
    status,
    total_amount
from {{ source('raw_ecommerce', 'orders') }}
