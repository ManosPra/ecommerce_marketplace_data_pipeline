{{ config(
    materialized='table',
    partition_by = 'date'
) }}

WITH vendor_data AS (
    SELECT *
    FROM {{ ref('dim_vendors') }} 
)

, order_data as (
    SELECT
        order_id
      , order_placed_at
      , vendor_id
      , item_price
      , item_quantity
    FROM {{ ref('fact_orders') }} 
)

SELECT
    DATE(order_placed_at) AS date
  , vendor_id
  , vendor_vertical
  , vendor_name
  , COUNT(DISTINCT order_id) AS total_orders
  , SUM(item_price*item_quantity) AS total_value
FROM order_data
LEFT JOIN vendor_data
    ON order_data.vendor_id = vendor_data.vendor_id
GROUP BY 1,2,3,4