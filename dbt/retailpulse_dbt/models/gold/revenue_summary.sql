SELECT

    SUM(total_amount) AS total_revenue,

    AVG(total_amount) AS average_order_value,

    COUNT(order_id) AS total_orders,

    SUM(qty) AS total_items_sold

FROM {{ ref('fact_sales')}}