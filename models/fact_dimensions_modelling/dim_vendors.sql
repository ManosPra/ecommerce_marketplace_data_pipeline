{{ config(
  materialized='table',
  unique_key='vendor_id'
) }}

SELECT
   vendor_id
 , vendor_name
 , vendor_address,
 , vendor_vertical
FROM ecommerce_db.raw_orders
GROUP BY 1,2,3,4