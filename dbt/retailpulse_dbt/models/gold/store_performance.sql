SELECT

    s.store_id,
    SUM(f.total_amount) AS total_revenue,
    AVG(f.total_amount) AS avg_transaction_value,
    SUM(f.qty) AS total_quantity,
    COUNT(f.order_id) AS total_orders

FROM {{ ref('fact_sales')}} f

JOIN {{ ref('dim_store')}} s
    ON f.store_sk = s.store_sk

GROUP BY
    s.store_id

ORDER BY total_revenue DESC