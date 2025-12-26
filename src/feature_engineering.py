import pandas as pd
from csv_cleaner import clean_csv

def create_features(orders_path, customers_path, sellers_path, order_items_path):
    """
    Load CSVs and create derived features for shipment delay prediction.

    Parameters:
    - orders_path: path to cleaned orders CSV with 'delayed' target
    - customers_path: path to customers CSV
    - sellers_path: path to sellers CSV
    - order_items_path: path to order items CSV

    Returns:
    - DataFrame with features and target
    """

    # Load CSVs
    orders = pd.read_csv(orders_path)
    customers = pd.read_csv(customers_path)
    sellers = pd.read_csv(sellers_path)
    order_items = pd.read_csv(order_items_path)

    # Strip column names to avoid whitespace issues
    orders.columns = orders.columns.str.strip()
    customers.columns = customers.columns.str.strip()
    sellers.columns = sellers.columns.str.strip()
    order_items.columns = order_items.columns.str.strip()

    # Convert timestamps
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
    orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

    # Time-based features
    orders['purchase_hour'] = orders['order_purchase_timestamp'].dt.hour
    orders['purchase_weekday'] = orders['order_purchase_timestamp'].dt.weekday
    orders['purchase_month'] = orders['order_purchase_timestamp'].dt.month
    orders['approval_lag_hours'] = (orders['order_approved_at'] - orders['order_purchase_timestamp']).dt.total_seconds() / 3600

    # Merge with order items to get seller_id and compute order-level aggregates
    order_items_agg = order_items.groupby('order_id').agg({
        'seller_id': 'first',             # assuming one seller per order; if multiple, may need adjustment
        'price': 'sum',
        'freight_value': 'sum',
        'order_item_id': 'count'
    }).reset_index().rename(columns={'order_item_id': 'num_items'})

    orders = orders.merge(order_items_agg, on='order_id', how='left')

    # Merge with sellers
    orders = orders.merge(
        sellers[['seller_id', 'seller_state', 'seller_city']],
        on='seller_id',
        how='left'
    )

    # Merge with customers
    orders = orders.merge(
        customers[['customer_id', 'customer_state', 'customer_city']],
        on='customer_id',
        how='left'
    )

    return orders

# Example usage
if __name__ == "__main__":
    orders_features = create_features(
        orders_path='/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/data/processed/olist_orders_with_target.csv',
        customers_path='/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/data/raw/olist_customers_dataset.csv',
        sellers_path='/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/data/raw/olist_sellers_dataset.csv',
        order_items_path='/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/data/raw/olist_order_items_dataset.csv'
    )
    
    # Save initial feature-engineered CSV
    interim_path = '/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/data/processed/olist_orders_features.csv'
    orders_features.to_csv(interim_path, index=False)
    print("Feature-engineered CSV saved to data/processed/")

    # Clean CSV before uploading to S3 / Athena
    clean_csv(
        input_path=interim_path,
        output_path='/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/data/processed/olist_orders_features_clean.csv',
        numeric_cols=[
            'delayed', 'purchase_hour', 'purchase_weekday', 'purchase_month',
            'approval_lag_hours', 'price', 'freight_value', 'num_items'
        ],
        categorical_cols=['customer_state', 'seller_state', 'customer_city', 'seller_city'],
        target_col='delayed'
    )

"""    # Save feature-engineered CSV
    orders_features.to_csv('/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/data/processed/olist_orders_features.csv', index=False)
    print("Feature-engineered CSV saved to data/processed/")"""
    
    
