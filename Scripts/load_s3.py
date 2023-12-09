# Loading into S3 , import boto3
import boto3
from io import StringIO

# Replace 'YOUR_ACCESS_KEY_ID' and 'YOUR_SECRET_ACCESS_KEY' with your actual credentials
aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
aws_region = 'us-east-2'  # Replace with your desired AWS region

# Replace 'your-unique-bucket-name' with a globally unique name for your bucket
bucket_name = 'cis4400-hw1'
object_key = 'nyc_hw1.csv'

# Configure AWS credentials
s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

# Convert DataFrame to CSV in-memory
csv_buffer = StringIO()
df_bin.to_csv(csv_buffer, index=False)

# Upload CSV file to S3 bucket
s3.Object(bucket_name, object_key).put(Body=csv_buffer.getvalue())

print(f"CSV file uploaded to S3 bucket: {bucket_name}/{object_key}")
