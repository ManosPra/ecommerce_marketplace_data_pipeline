import io
import pandas as pd
import requests
from pandas import DataFrame
import os
from faker import Faker
import random
import hashlib


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


fake = Faker()
@data_loader
def generate_fake_data(**kwargs) -> DataFrame:
    
# Generate and insert data for orders
    orders_data_raw = []
    vendor_verticals = ['Electronics', 'Books', 'Fashion', 'House and garden', 'Sports', 'Auto-moto', 'Health and beauty']
    for i in range(250000):
        order_id = hashlib.sha256(str(i).encode()).hexdigest()
        order_placed_at = fake.date_time_between(start_date='-3y', end_date='now')
        order_rating = random.randint(1, 5) if random.random() < 0.8 else None
        vendor_id = hashlib.sha256(str(random.randint(1, 20000)).encode()).hexdigest()
        vendor_name = fake.company()
        vendor_address = fake.address()
        vendor_vertical = random.choice(vendor_verticals)
        customer_id = hashlib.sha256(str(random.randint(1,1000000)).encode()).hexdigest()
        customer_registered_at = fake.date_time_between(start_date='-5y', end_date='now')
        item_sku = fake.uuid4()
        item_name = fake.word()
        item_price = round(random.uniform(10, 1000), 2)
        item_quantity = random.randint(1, 10)
        orders_data_raw.append({'order_id':order_id,'order_placed_at': order_placed_at,'order_rating': order_rating
                               ,'vendor_id':vendor_id,'vendor_name': vendor_name, 'vendor_address': vendor_address, 'vendor_vertical': vendor_vertical
                               ,'customer_id':customer_id,'customer_registered_at': customer_registered_at
                              ,'item_sku': item_sku, 'item_name': item_name,'item_price': item_price, 'item_quantity': item_quantity
                              })
    orders_df = pd.DataFrame(orders_data_raw)

    return (orders_df)
