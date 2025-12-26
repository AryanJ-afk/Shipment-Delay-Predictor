import boto3
import time

REGION = "ap-south-1"

ROLE_ARN = "arn:aws:iam::511479743830:role/service-role/AmazonSageMakerAdminIAMExecutionRole"

TRAIN_S3_URI = "s3://shipment-delay-project/ml-data/train/"
OUTPUT_S3_URI = "s3://shipment-delay-project/models/"

JOB_NAME = f"shipment-delay-xgb-{int(time.time())}"

sm = boto3.client("sagemaker", region_name=REGION)

response = sm.create_training_job(
    TrainingJobName=JOB_NAME,
    RoleArn=ROLE_ARN,
    AlgorithmSpecification={
        "TrainingImage": "720646828776.dkr.ecr.ap-south-1.amazonaws.com/sagemaker-xgboost:1.7-1",
        "TrainingInputMode": "File",
    },
    InputDataConfig=[
        {
            "ChannelName": "train",
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": TRAIN_S3_URI,
                    "S3DataDistributionType": "FullyReplicated",
                }
            },
            "ContentType": "text/csv",
        }
    ],
    OutputDataConfig={
        "S3OutputPath": OUTPUT_S3_URI
    },
    ResourceConfig={
        "InstanceType": "ml.m5.large",
        "InstanceCount": 1,
        "VolumeSizeInGB": 30,
    },
    StoppingCondition={
        "MaxRuntimeInSeconds": 3600
    },
    HyperParameters={
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "num_round": "100",
        "max_depth": "5",
        "eta": "0.2",
        "subsample": "0.8",
        "verbosity": "1",
    },
)

print(f"Training job started: {JOB_NAME}")
