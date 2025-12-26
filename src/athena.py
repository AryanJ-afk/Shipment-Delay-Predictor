import boto3
import pandas as pd
import time

REGION         = "ap-south-1"
BUCKET         = "shipment-delay-project"          
ATHENA_DB_NAME = "shipment_db"    
ATHENA_OUTPUT  = f"s3://{BUCKET}/athena-results/"

session = boto3.Session(region_name=REGION)
athena = session.client("athena")

query = """
CREATE TABLE sagemaker_orders AS
SELECT
    delayed,
    purchase_hour,
    purchase_weekday,
    purchase_month,
    approval_lag_hours,
    price,
    freight_value,
    num_items,
    customer_state,
    seller_state
FROM cleaned
"""

resp = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": ATHENA_DB_NAME},
        ResultConfiguration={"OutputLocation": ATHENA_OUTPUT},
    )
qid = resp["QueryExecutionId"]

while True:
    time.sleep(2)
    q = athena.get_query_execution(QueryExecutionId=qid)
    state = q["QueryExecution"]["Status"]["State"]
    if state in ("SUCCEEDED", "FAILED", "CANCELLED"):
        if state != "SUCCEEDED":
            raise RuntimeError(q)
        break

