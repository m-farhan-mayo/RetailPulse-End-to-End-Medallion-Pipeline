SELECT DISTINCT

    {{ generate_surrogate_key(['store_id'])}} AS store_sk,

    store_id

FROM {{ ref('stg_sales') }}