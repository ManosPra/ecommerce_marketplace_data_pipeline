{{ config(
  materialized='table'
  ) }}

SELECT
   item_sku
 , vendor_id
 , item_name
FROM ecommerce_db.raw_orders
GROUP BY 1,2,3