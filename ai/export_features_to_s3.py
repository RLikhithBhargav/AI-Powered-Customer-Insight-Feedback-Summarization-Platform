# File: ai/export_features_to_s3.py

import os
import pandas as pd
import snowflake.connector
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='ai/creds.env')

# --- Snowflake credentials ---
sf_user = os.getenv("SNOWFLAKE_USER")
sf_password = os.getenv("SNOWFLAKE_PASSWORD")
sf_account = os.getenv("SNOWFLAKE_ACCOUNT")

# --- AWS credentials ---
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION", "us-east-2")  # default fallback
s3_bucket = "customer-insights-platform"           # TODO: replace with your real bucket
s3_key = "quicksight/customer_features.csv"

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=sf_user,
    password=sf_password,
    account=sf_account,
    warehouse="demo_wh",
    database="customer_insights",
    schema="analytics"
)

# Pull data from fct_customer_features
print("📥 Pulling data from Snowflake...")
query = "SELECT * FROM fct_customer_features"
df = pd.read_sql(query, conn)

# Save locally
local_file = "ai/customer_features.csv"
df.to_csv(local_file, index=False)
print(f"💾 Saved locally to {local_file}")

# Upload to S3
print("☁️ Uploading to S3...")
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

s3.upload_file(local_file, s3_bucket, s3_key)
print(f"✅ Uploaded to s3://{s3_bucket}/{s3_key}")
