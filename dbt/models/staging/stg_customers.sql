{{ config(materialized='view') }}

SELECT
    customer_id,
    name,
    signup_date,
    age,
    location,
    status
FROM {{ source('raw_data', 'customers') }}
