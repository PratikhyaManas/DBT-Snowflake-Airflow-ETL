-- Fact table for sales analytics
select
    o.order_id,
    o.customer_id,
    o.order_date,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) as line_total,
    o.status
from {{ ref('stg_orders') }} o
join {{ ref('stg_order_items') }} oi
    on o.order_id = oi.order_id
