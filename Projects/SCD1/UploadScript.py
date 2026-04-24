import boto3
import yaml
import os

# Load AWS credentials from YAML file
with open('AWS_Credentials.yml', 'r') as file:
    aws_credentials = yaml.safe_load(file)

aws_access_key_id = aws_credentials['aws_access_key_id']
aws_secret_access_key = aws_credentials['aws_secret_access_key']
aws_region_name = aws_credentials['aws_region_name']

# Initialize AWS session
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region_name
)

# Update these values
file_name = "customer_full_data.csv"  
bucket_name = "dea-scd1project-277361137027-us-east-1-an" 
folder_name = "data" 

# Create S3 client
s3_client = session.client('s3')

# Build S3 key safely
key = os.path.join(folder_name, file_name) if folder_name else file_name

try:
    # Upload file to S3
    s3_client.upload_file(
        Filename=file_name,
        Bucket=bucket_name,
        Key=key
    )
    print(f"{file_name} uploaded successfully to {bucket_name}/{key}")

except FileNotFoundError:
    print("The specified file was not found locally.")

except Exception as e:
    print(f"An error occurred: {e}")