SELECT DISTINCT

    {{ generate_surrogate_key(['sale_date'])}} AS date_sk,

    sale_date,

    EXTRACT(YEAR FROM sale_date) AS year,
    EXTRACT(MONTH FROM sale_date) AS month,
    EXTRACT(DAY FROM sale_date) AS day

FROM {{ ref('stg_sales') }}