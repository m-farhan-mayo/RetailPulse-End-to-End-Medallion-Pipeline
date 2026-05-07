SELECT 

    p.product_id,

    SUM(f.total_amount) AS total_revenue,
    SUM(f.qty) AS total_quantity_sold,

    COUNT(f.order_id) AS total_orders

FROM {{ ref('fact_sales') }} f

JOIN {{ ref('dim_product') }} p
    ON f.product_sk = p.product_sk

GROUP BY
    p.product_id

ORDER BY total_revenue DESC