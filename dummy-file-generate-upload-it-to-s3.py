import boto3
import os
import random
import string

# Replace these with your own AWS S3 bucket name and region
region_name = 'us-east-1'  # North Virginia region
bucket_name = 'demo-s3-replication-source'

# Create an S3 client using the default credentials in your environment
s3 = boto3.client('s3', region_name=region_name)

# Function to generate random data and write it to a file
def generate_and_write_file(file_name, size_mb):
    data = ''.join(random.choices(string.ascii_letters + string.digits, k=int(size_mb * 1024 * 1024)))
    with open(file_name, 'w') as file:
        file.write(data)

# Function to upload a file to S3
def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    try:
        response = s3.upload_file(file_name, bucket, object_name)
        print(f'Successfully uploaded {file_name} to {bucket}/{object_name}')
    except Exception as e:
        print(f'Error uploading {file_name} to {bucket}/{object_name}: {e}')

# List of files to generate, write, and upload
files_to_generate = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt', 'file5.txt',
                      'file6.txt', 'file7.txt', 'file8.txt', 'file9.txt', 'file10.txt']

# Generate, write, and upload each file to the S3 bucket
for file_to_generate in files_to_generate:
    file_size_mb = random.uniform(1, 2)  # Random size between 1 MB and 2 MB
    generate_and_write_file(file_to_generate, file_size_mb)
    upload_file(file_to_generate, bucket_name)
    os.remove(file_to_generate)  # Remove the local file after upload to keep things clean
