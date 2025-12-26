import boto3
import pandas as pd
from sklearn.model_selection import train_test_split
import os

def upload_to_s3(local_file, bucket, s3_path):
    s3 = boto3.client('s3')
    s3.upload_file(local_file, bucket, s3_path)
    print(f"Uploaded {local_file} to s3://{bucket}/{s3_path}")

def prepare_and_upload(csv_file, bucket, s3_prefix, test_size=0.2, random_state=42):
    # Read CSV
    df = pd.read_csv(csv_file)

    # Split into train and validation
    train_df, val_df = train_test_split(df, test_size=test_size, random_state=random_state, stratify=df['delayed'])

    # Save locally
    os.makedirs('tmp', exist_ok=True)
    train_file = 'tmp/train.csv'
    val_file = 'tmp/validation.csv'
    train_df.to_csv(train_file, index=False)
    val_df.to_csv(val_file, index=False)

    # Upload to S3
    upload_to_s3(train_file, bucket, f"{s3_prefix}/train/train.csv")
    upload_to_s3(val_file, bucket, f"{s3_prefix}/validation/validation.csv")

    print("Train and validation CSVs are ready in S3 for SageMaker.")


if __name__ == "__main__":
    # === PARAMETERS (set directly here) ===
    csv_file = "/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/src/sagemaker_orders_local.csv"  # local CSV with features and target
    bucket = "shipment-delay-project"        # your S3 bucket
    s3_prefix = "ml-data"                    # S3 folder for train/validation data
    test_size = 0.2                          # validation split ratio
    random_state = 42                        # random seed

    prepare_and_upload(csv_file, bucket, s3_prefix, test_size, random_state)
