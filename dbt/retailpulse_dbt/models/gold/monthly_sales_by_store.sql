SELECT 

    d.year,
    d.month,

    s.store_id,

    SUM(f.total_amount) AS monthly_sales,
    SUM(f.qty) AS total_quantity_sold,
    COUNT(f.order_id) AS total_orders

FROM {{ ref('fact_sales') }} AS f

JOIN {{ ref('dim_store')}} AS s
    ON f.store_sk = s.store_sk

JOIN {{ ref('dim_date')}} d
    ON f.date_sk = d.date_sk

GROUP BY
    d.year,
    d.month,
    s.store_id