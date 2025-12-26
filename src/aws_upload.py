import boto3
import os

def upload_folder_to_s3(local_folder, bucket_name, s3_folder='raw'):
    s3 = boto3.client('s3')
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_folder)
            s3_path = f"{s3_folder}/{relative_path}"
            s3.upload_file(local_path, bucket_name, s3_path)
            print(f"Uploaded {local_path} to s3://{bucket_name}/{s3_path}")

# Upload the data to S3
upload_folder_to_s3('/Users/aryanjha/Desktop/MsAI/Personal/Python/shipment_delay_prediction/data/', 'shipment-delay-project', 'data')
