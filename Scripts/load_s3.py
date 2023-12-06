# Loading into S3 , import boto3
import boto3
from io import StringIO

# Replace 'YOUR_ACCESS_KEY_ID' and 'YOUR_SECRET_ACCESS_KEY' with your actual credentials
aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
aws_region = 'us-east-2'  # Replace with your desired AWS region

# Configure AWS credentials
s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

# Replace 'your-unique-bucket-name' with a globally unique name for your bucket
bucket_name = 'your-unique-bucket-name'

# Convert DataFrame to CSV in-memory
csv_buffer = StringIO()
df_bin.to_csv(csv_buffer, index=False)

# Configure AWS credentials
s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

# Upload CSV file to S3 bucket
object_key = 'nyc_hw.csv'
s3.Bucket(bucket_name).put_object(Key=object_key, Body=csv_buffer.getvalue())

print(f"CSV file uploaded to S3 bucket: {bucket_name}/{object_key}")
