import boto3
import json
import time
import numpy as np

# ==========================
# CONFIG
# ==========================

REGION = "ap-south-1"
ENDPOINT_NAME = "shipment-delay-endpoint-1766739864"
THRESHOLD = 0.6  # business decision threshold

# ==========================
# CLIENT
# ==========================

runtime = boto3.client("sagemaker-runtime", region_name=REGION)

# Example input row
payload = "0.35,1,0,12,450,0\n" 

# ==========================
# INVOKE ENDPOINT
# ==========================

start_time = time.time()

response = runtime.invoke_endpoint(
    EndpointName=ENDPOINT_NAME,
    ContentType="text/csv",
    Body=payload,
)

latency_ms = (time.time() - start_time) * 1000

# ==========================
# PARSE OUTPUT
# ==========================

prediction = float(response["Body"].read().decode("utf-8").strip())

decision = "DELAY_RISK" if prediction >= THRESHOLD else "ON_TIME"

# ==========================
# LOG OUTPUT
# ==========================

print("Prediction score :", round(prediction, 4))
print("Decision         :", decision)
print("Latency (ms)     :", round(latency_ms, 2))
