{{ config(materialized='view') }}

SELECT
    ticket_id,
    customer_id,
    created_at,
    text
FROM {{ source('raw_data', 'support_tickets') }}
