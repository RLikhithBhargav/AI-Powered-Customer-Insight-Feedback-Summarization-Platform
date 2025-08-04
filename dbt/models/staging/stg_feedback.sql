{{ config(materialized='view') }}

SELECT
    feedback_id,
    customer_id,
    date,
    rating,
    comment
FROM {{ source('raw_data', 'feedback') }}
