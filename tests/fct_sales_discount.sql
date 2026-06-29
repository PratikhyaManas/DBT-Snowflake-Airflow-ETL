select
    *
from {{ ref('fct_sales') }}
where item_discount_amount > 0
