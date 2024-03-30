{{ config(
  materialized='table',
  unique_key='order_id'
) }}

SELECT
    order_id
  , order_placed_at
  , order_rating
  , vendor_id
  , customer_id
  , item_sku
  , item_price
  , item_quantity
FROM ecommerce_db.raw_orders