{{ config(
  materialized='table',
  unique_key='customer_id'
) }}

SELECT
   customer_id
 , customer_registered_at
FROM ecommerce_db.raw_orders
GROUP BY 1,2