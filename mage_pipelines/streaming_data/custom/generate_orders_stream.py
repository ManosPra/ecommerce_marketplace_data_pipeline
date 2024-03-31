if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

import time
import json
import random
from google.cloud import pubsub_v1
from google.cloud import bigquery
import hashlib
from faker import Faker
from datetime import datetime
import pandas as pd

project_id = 'gothic-avenue-412217'
topic_name = 'orders_topic'
# Create a publisher client
publisher = pubsub_v1.PublisherClient()
# Get the full topic path
topic_path = publisher.topic_path(project_id, topic_name)

fake = Faker()
@custom
def transform_custom(*args, **kwargs):
    # Pre-generate a list of 100 vendor addresses and company names
    vendor_addresses = [fake.address() for _ in range(100)]
    vendor_names = [fake.company() for _ in range(100)]
    vendor_verticals = ['Electronics', 'Books', 'Fashion', 'House and garden', 'Sports', 'Auto-moto', 'Health and beauty']

    for i in range(500000,510000):
        # Generate a synthetic orders data
        order_id = hashlib.sha256(str(i).encode()).hexdigest()
        order_placed_at = datetime.now().isoformat()
        order_rating = random.randint(1, 5) if random.random() < 0.8 else None
        vendor_id = hashlib.sha256(str(random.randint(21000, 22000)).encode()).hexdigest()
        vendor_name = random.choice(vendor_names)
        vendor_address = random.choice(vendor_addresses)
        vendor_vertical = random.choice(vendor_verticals)
        customer_id = hashlib.sha256(str(random.randint(1,1000000)).encode()).hexdigest()
        item_sku = fake.uuid4()
        item_name = fake.word()
        item_price = round(random.uniform(10, 1000), 2)
        item_quantity = random.randint(1, 10)

        # Create a dictionary representing the order message
        order_message = {
            'order_id': order_id,
            'order_placed_at': order_placed_at,
            'order_rating': order_rating,
            'vendor_id': vendor_id,
            'vendor_name': vendor_name,
            'vendor_address' : vendor_address,
            'vendor_vertical' : vendor_vertical,
            'customer_id': customer_id,
            'item_sku': item_sku,
            'item_name': item_name,
            'item_price': item_price,
            'item_quantity': item_quantity
        }


        # Publish the message to the topic
        publisher.publish(topic_path, data=json.dumps(order_message).encode('utf-8'))
        print(f"Published message: {order_message}")
        time.sleep(random.randint(1, 5))  # Simulate streaming by waiting random time between messages
    return {}