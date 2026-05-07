SELECT DISTINCT

    {{ generate_surrogate_key(['product_id'])}} AS product_sk,

    product_id,
    price
    
FROM {{ ref('stg_sales') }}