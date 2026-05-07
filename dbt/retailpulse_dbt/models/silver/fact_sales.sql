SELECT 

    order_id,

    {{ generate_surrogate_key(['product_id'])}} AS product_sk,
    {{ generate_surrogate_key(['store_id'])}} AS store_sk,
    {{ generate_surrogate_key(['sale_date'])}} AS date_sk,

    qty,
    price,
    total_amount

FROM {{ ref('stg_sales') }}