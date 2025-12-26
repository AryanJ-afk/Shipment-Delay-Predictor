import pandas as pd

orders = pd.read_csv('/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/data/olist_orders_dataset.csv')
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])

orders['delay_days'] = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']).dt.days

orders.isnull().sum()

print(orders['delay_days'].describe())
print("Number of early deliveries:", (orders['delay_days'] < 0).sum())
print("Number of delayed deliveries:", (orders['delay_days'] > 0).sum())

orders['delayed'] = (orders['delay_days'] > 0).astype(int)
orders['delayed'].value_counts()


orders = orders[orders['order_status'] == 'delivered']
orders = orders.dropna(subset=['order_delivered_customer_date', 'order_estimated_delivery_date'])
orders = orders.drop_duplicates(subset=['order_id'])


orders.to_csv('/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/data/processed/olist_orders_with_target.csv', index=False)
