select
    line_items.order_item_key,
    line_items.order_key,
    line_items.extended_price,
    line_items.discount,
    {{ discounted_amount('line_items.extended_price', 'line_items.discount') }} as item_discount_amount
from {{ ref('stg_orders') }} as orders
join {{ ref('stg_order_items') }} as line_items
    on orders.order_key = line_items.order_key
