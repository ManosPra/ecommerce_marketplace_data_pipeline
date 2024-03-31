import pandas as pd
from pandas import DataFrame


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def duplicates_check(df: DataFrame) -> DataFrame:
    # Drop rows where customer_id, vendor_id, and order_placed_at are the same, keep only the first occurrence
    df.drop_duplicates(subset=['customer_id', 'vendor_id', 'order_placed_at'], keep='first', inplace=True)

    return df


def customers_check(df: DataFrame) -> DataFrame:
    df['order_placed_at'] = pd.to_datetime(df['order_placed_at'])
    df['customer_registered_at'] = pd.to_datetime(df['customer_registered_at'])

    # Keep only rows where order_placed_at >= customer_registered_at
    df = df[df['order_placed_at'] >= df['customer_registered_at']]

    return df

def fix_duplicate_vendors(df:DataFrame) -> DataFrame:
    # Group by vendor_id and aggregate vendor_name, vendor_address, and vendor_vertical
    grouped = df.groupby('vendor_id').agg({
        'vendor_name': 'first',
        'vendor_address': 'first',
        'vendor_vertical': 'first'
    }).reset_index() # for each unique vendor_id keep a single combination of name, address and vertical

    merged_df = pd.merge(df, grouped, on='vendor_id', suffixes=('', '_first'))
    # Replace vendor_name, vendor_address, and vendor_vertical with the first occurrence for each vendor_id
    merged_df['vendor_name'] = merged_df['vendor_name_first']
    merged_df['vendor_address'] = merged_df['vendor_address_first']
    merged_df['vendor_vertical'] = merged_df['vendor_vertical_first']

    # Drop the duplicated columns
    merged_df.drop(['vendor_name_first', 'vendor_address_first', 'vendor_vertical_first'], axis=1, inplace=True)

    return merged_df


def fix_duplicate_customers(df:DataFrame) -> DataFrame:
    # Group by vendor_id and aggregate vendor_name, vendor_address, and vendor_vertical
    grouped = df.groupby('customer_id').agg({
        'customer_registered_at': 'first'
    }).reset_index() # for each customer_id keep a single customer_registered_at field

    # Merge the aggregated data back to the original DataFrame based on vendor_id
    merged_df = pd.merge(df, grouped, on='customer_id', suffixes=('', '_first'))

    # Replace vendor_name, vendor_address, and vendor_vertical with the first occurrence for each vendor_id
    merged_df['customer_registered_at'] = merged_df['customer_registered_at_first']

    # Drop the duplicated columns
    merged_df.drop(['customer_registered_at_first'], axis=1, inplace=True)

    return merged_df



def item_skus_check(df: DataFrame) -> DataFrame:

    # Group by item_sku and keep the first occurrence of item_name
    grouped_items = df.groupby('item_sku').agg({
        'item_name': 'first'
    }).reset_index()

    # Create a dictionary mapping item_sku to the first occurrence of item_name
    item_name_mapping = grouped_items.set_index('item_sku')['item_name'].to_dict()
    # Replace item_name in the original DataFrame with the first occurrence for each item_sku
    df['item_name'] = df['item_sku'].map(item_name_mapping)

    return df




@transformer
def transform_df(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Args:
        df (DataFrame): Data frame from parent block.

    Returns:
        DataFrame: Transformed data frame
    """

    return fix_duplicate_vendors(fix_duplicate_customers(item_skus_check(customers_check(duplicates_check(df)))))
