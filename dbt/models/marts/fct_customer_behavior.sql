{{ config(materialized='table') }}

WITH joined_data AS (
  SELECT
    c.customer_id,
    c.name,
    COUNT(DISTINCT t.txn_id) AS total_transactions,
    SUM(t.amount) AS total_spent,
    AVG(f.rating) AS avg_feedback_rating,
    COUNT(DISTINCT s.ticket_id) AS support_ticket_count
  FROM {{ ref('stg_customers') }} c
  LEFT JOIN {{ ref('stg_transactions') }} t
    ON c.customer_id = t.customer_id
  LEFT JOIN {{ ref('stg_feedback') }} f
    ON c.customer_id = f.customer_id
  LEFT JOIN {{ ref('stg_support_tickets') }} s
    ON c.customer_id = s.customer_id
  GROUP BY c.customer_id, c.name
)

SELECT * FROM joined_data
