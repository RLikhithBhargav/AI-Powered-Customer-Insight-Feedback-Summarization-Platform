{{ config(materialized='view') }}

SELECT
    txn_id,
    customer_id,
    txn_date,
    amount,
    category
FROM {{ source('raw_data', 'transactions') }}
