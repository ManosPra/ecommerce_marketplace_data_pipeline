from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from pandas import DataFrame
import os
import json
from google.oauth2 import service_account


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:
    
    project_id = 'gothic-avenue-412217'
    dataset_id = 'ecommerce_db'
    client = bigquery.Client(project=project_id)

    # Construct a full Dataset object to send to the API
    dataset = bigquery.Dataset(f"{client.project}.{dataset_id}")
    dataset = client.create_dataset(dataset, exists_ok=True)


    schema = [
    bigquery.SchemaField('order_id', 'STRING'),
    bigquery.SchemaField('order_placed_at', 'TIMESTAMP'),
    bigquery.SchemaField('order_rating', 'INTEGER'),
    bigquery.SchemaField('vendor_id', 'STRING'),
    bigquery.SchemaField('vendor_name', 'STRING'),
    bigquery.SchemaField('vendor_address', 'STRING'),
    bigquery.SchemaField('vendor_vertical', 'STRING'),
    bigquery.SchemaField('customer_id', 'STRING'),
    bigquery.SchemaField('customer_registered_at', 'TIMESTAMP'),
    bigquery.SchemaField('item_sku', 'STRING'),
    bigquery.SchemaField('item_name', 'STRING'),
    bigquery.SchemaField('item_price', 'FLOAT'),
    bigquery.SchemaField('item_quantity', 'INTEGER')
    ]

    table_name = 'raw_orders'
    table_ref = client.dataset(dataset_id).table(table_name)
    table = bigquery.Table(table_ref, schema=schema)

    table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field='order_placed_at'
    )

    # If the table exists, delete it
    try:
        table = client.get_table(table_ref)
        print("Table {} already exists.".format(dataset_id + '.' + table_name))
        client.delete_table(table_ref)
        print("Table {} deleted.".format(dataset_id + '.' + table_name))
    except Exception as e:
        if isinstance(e, NotFound):
            print("Table {} does not exist. Creating now ...".format(dataset_id + '.' + table_name))
        else:
            print(f"An error occurred: {e}")

    # Create the table
    table = client.create_table(table)

    # Load the DataFrame into the BigQuery table
    job = client.load_table_from_dataframe(
        df, table_ref, job_config=bigquery.LoadJobConfig()
    )
    job.result()  # Wait for the job to complete
    print("Table {} created".format(dataset_id + '.' + table_name))