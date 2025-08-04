{{ config(materialized='table') }}

WITH base AS (
  SELECT
    c.customer_id,
    c.name,
    c.signup_date,
    CURRENT_DATE() - c.signup_date AS customer_tenure_days,

    COUNT(DISTINCT t.txn_id) AS txn_count,
    SUM(t.amount) AS total_spent,
    AVG(t.amount) AS avg_order_value,
    MAX(t.txn_date) AS last_txn_date,
    DATEDIFF('day', MAX(t.txn_date), CURRENT_DATE()) AS days_since_last_txn,

    AVG(f.rating) AS avg_feedback_rating,
    COUNT(DISTINCT s.ticket_id) AS support_ticket_count
  FROM {{ ref('stg_customers') }} c
  LEFT JOIN {{ ref('stg_transactions') }} t ON c.customer_id = t.customer_id
  LEFT JOIN {{ ref('stg_feedback') }} f ON c.customer_id = f.customer_id
  LEFT JOIN {{ ref('stg_support_tickets') }} s ON c.customer_id = s.customer_id
  GROUP BY 1, 2, 3
)

SELECT *,
  CASE 
    WHEN days_since_last_txn > 90 THEN 'High Risk'
    WHEN days_since_last_txn BETWEEN 31 AND 90 THEN 'Medium Risk'
    ELSE 'Low Risk'
  END AS churn_risk_category
FROM base
