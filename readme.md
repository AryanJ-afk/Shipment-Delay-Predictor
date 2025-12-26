# Project Description

This project implements an end-to-end machine learning pipeline on AWS SageMaker to predict whether a shipment will be delayed based on historical shipment features.

The workflow covers:

- Model training using a managed SageMaker training job (XGBoost)
- Model packaging and deployment to a real-time inference endpoint
- Predictions with configurable thresholding for binary classification

The system is designed to mirror a production-style MLOps workflow, including cloud-based training, artifact storage in Amazon S3, and live inference via a hosted endpoint.

# Architecture and Workflow Overview

The project follows a standard cloud-based machine learning lifecycle using AWS-managed services.

1. Data Storage

- Training data is stored in Amazon S3 as CSV files.
- SageMaker accesses the data directly from S3 during training.

2. Model Training

- A SageMaker training job is launched using the built-in XGBoost container.
- Training artifacts (model.tar.gz) are automatically saved to S3.
- Hyperparameters are configured at job creation time.

3. Model Deployment

- The trained model is registered as a SageMaker model.
- A real-time inference endpoint is created using a managed instance.
- SageMaker handles container orchestration and scaling.

4. Real-Time Inference

- Incoming requests are sent to the endpoint as CSV payloads.
- The model returns a probability score indicating likelihood of delay.
- A configurable threshold converts this score into a binary prediction

# Module/File Descriptions

csv_cleaner.py – Cleans and preprocesses CSV files by converting numeric columns, stripping categorical text, optionally reordering the target column, and saving the cleaned output.

data_cleaning.py – Processes raw order data by calculating delivery delays, creating a binary delay target, filtering delivered orders, handling missing/duplicate entries, and saving the cleaned dataset.

feature_engineering.py – Generates derived features from orders, customers, sellers, and order items datasets, merges them, and outputs a cleaned, feature-rich CSV for shipment delay prediction.

aws_upload.py – Uploads a local folder and its contents to a specified S3 bucket, preserving folder structure.

athena.py – Executes an AWS Athena query to create a table with selected features from the cleaned dataset and stores the results in an S3 bucket.

get_table.py – Exports an AWS Athena table to a local CSV by executing a query and retrieving the results programmatically.

sagemaker_upload.py – Splits a feature dataset into training and validation sets and uploads them to S3 for use in SageMaker training.

train.py – Launches an AWS SageMaker training job using XGBoost to train a binary classifier on the shipment delay dataset.

endpoint.py – Creates a SageMaker model from trained artifacts, configures an endpoint, and deploys it for real-time inference.

prediction.py – Sends input data to a deployed SageMaker endpoint, retrieves the predicted delay probability, and outputs a binary decision with latency.

# Data

This project uses the Brazilian E‑Commerce Public Dataset by Olist, a publicly available dataset from Kaggle containing real e‑commerce data from ~100,000 orders placed between 2016 and 2018 on the Olist marketplace platform in Brazil.
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/discussion?sort=hotness

The dataset includes multiple related CSV files that provide a comprehensive view of e‑commerce transactions, customer and seller information, and purchased items. Key tables used in this project include:

- olist_orders_dataset.csv – Order records with status and timestamp fields for purchase, approval, estimated delivery, and actual delivery.
- - Used to compute delay_days (difference between delivered and estimated delivery dates).
- - Filtered to only include delivered orders. 

- olist_order_items_dataset.csv – Items within each order, including seller_id, price, and freight_value.
- - Aggregated per order to compute total order price, freight value, and number of items. 

- olist_customers_dataset.csv – Customer identifiers and location (customer_state, customer_city).
- - Merged to associate customer location with each order. 

- olist_sellers_dataset.csv – Seller identifiers and location (seller_state, seller_city).
- - Merged to associate seller location with each order.

# Results

AUC: 0.6775681186731435
Accuracy: 0.932258733284959
F1-score: 0.0015278838808250573

# 3. Notes / Limitations

- Model F1-score is low due to class imbalance.  
- Current pipeline is intended as a demo of SageMaker deployment rather than feature engineering and performance boosting.  
 

# 4. Future Improvements

- Use SMOTE or class-weighted XGBoost to improve F1-score.  
- Include more derived features (distance, time lags, seller metrics).  
- Automate Athena → SageMaker → Deployment in a single script or notebook.  