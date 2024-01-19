import boto3
import csv
import os
from io import StringIO
from datetime import datetime, timezone

def lambda_handler(event, context):
    # Set your AWS region
    region = 'us-west-2'  # Change this to your desired region (Oregon region in this case)

    # Set your S3 bucket name
    bucket_name = 'S3_Bucket_Name'

    # Initialize the AWS SDK for EC2 and S3
    ec2 = boto3.client('ec2', region_name=region)
    s3 = boto3.client('s3')

    # Get all snapshots in the region
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Filter out the active snapshots (exclude deleted and previous versions)
    active_snapshots = [snapshot for snapshot in response['Snapshots'] if snapshot['State'] == 'completed']

    # Create a CSV string from the snapshot data
    csv_data = create_csv_string(active_snapshots)

    # Upload the CSV data to S3
    upload_to_s3(bucket_name, 'snapshots.csv', csv_data)

    return {
        'statusCode': 200,
        'body': f'Snapshot information exported successfully. CSV data uploaded to S3 bucket: {bucket_name}/snapshots.csv'
    }

def create_csv_string(data):
    # Create a CSV string from the snapshot data
    csv_string = 'SnapshotId,VolumeId,StartTime,AgeInDays,Description\n'

    for snapshot in data:
        age_in_days = calculate_age_in_days(snapshot['StartTime'])
        csv_string += f"{snapshot['SnapshotId']},{snapshot['VolumeId']},{str(snapshot['StartTime'])},{age_in_days},{snapshot['Description']}\n"

    return csv_string

def calculate_age_in_days(start_time):
    # Calculate the age of a snapshot in days
    current_time = datetime.now(timezone.utc)
    delta = current_time - start_time
    return delta.days

def upload_to_s3(bucket, key, data):
    # Upload data to S3 bucket
    s3 = boto3.client('s3')
    s3.put_object(Body=data, Bucket=bucket, Key=key)
