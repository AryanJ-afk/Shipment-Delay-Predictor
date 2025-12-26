import boto3
import time

# ==========================
# CONFIG
# ==========================

REGION = "ap-south-1"

ROLE_ARN = "arn:aws:iam::511479743830:role/service-role/AmazonSageMakerAdminIAMExecutionRole"

# From completed training job
MODEL_ARTIFACT_S3 = "s3://shipment-delay-project/models/shipment-delay-xgb-1766739634/output/model.tar.gz"

# XGBoost image for ap-south-1
IMAGE_URI = "720646828776.dkr.ecr.ap-south-1.amazonaws.com/sagemaker-xgboost:1.7-1"

INSTANCE_TYPE = "ml.m5.large"

TIMESTAMP = int(time.time())
MODEL_NAME = f"shipment-delay-model-{TIMESTAMP}"
ENDPOINT_CONFIG_NAME = f"shipment-delay-config-{TIMESTAMP}"
ENDPOINT_NAME = f"shipment-delay-endpoint-{TIMESTAMP}"

# ==========================
# CLIENT
# ==========================

sm = boto3.client("sagemaker", region_name=REGION)

# ==========================
# CREATE MODEL
# ==========================

sm.create_model(
    ModelName=MODEL_NAME,
    ExecutionRoleArn=ROLE_ARN,
    PrimaryContainer={
        "Image": IMAGE_URI,
        "ModelDataUrl": MODEL_ARTIFACT_S3,
    },
)

print(f"Model created: {MODEL_NAME}")

# ==========================
# ENDPOINT CONFIG
# ==========================

sm.create_endpoint_config(
    EndpointConfigName=ENDPOINT_CONFIG_NAME,
    ProductionVariants=[
        {
            "VariantName": "AllTraffic",
            "ModelName": MODEL_NAME,
            "InitialInstanceCount": 1,
            "InstanceType": INSTANCE_TYPE,
            "InitialVariantWeight": 1.0,
        }
    ],
)

print(f"Endpoint config created: {ENDPOINT_CONFIG_NAME}")

# ==========================
# CREATE ENDPOINT
# ==========================

sm.create_endpoint(
    EndpointName=ENDPOINT_NAME,
    EndpointConfigName=ENDPOINT_CONFIG_NAME,
)

print(f"Endpoint creation started: {ENDPOINT_NAME}")
print("Status: Creating (this takes ~5–10 minutes)")
