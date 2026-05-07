WITH source AS (

    SELECT *
    FROM {{ source('clean', 'sales_clean') }}

),

transformed AS (

    SELECT

        order_id,
        COALESCE(store_id, -1) AS store_id,
        product_id,

        qty,
        price,

        CAST(date AS DATE) AS sale_date,

        qty * price AS total_amount

    FROM source

)

SELECT *
FROM transformed