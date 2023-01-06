import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from helper_functions import read_config
import json


def create_s3_bucket(s3_client: boto3.client, s3_bucket_name: str, region: str) -> dict:
    """Creates an S3 bucket if it doesn't already exist.
    Parameters:
        s3_client: Object representing a session with S3
        s3_bucket_name: Name of S3 bucket to create
        region: The AWS region to store the bucket in
    Returns:
        Response to the create attempt.
    """
    try:
        response = s3_client.create_bucket(
            ACL="public-read", Bucket=s3_bucket_name, CreateBucketConfiguration={"LocationConstraint": region}
        )
    except ClientError as e:
        if not (
            e.response["Error"]["Code"] == "BucketAlreadyExists"
            or e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou"
        ):
            raise
    else:
        return response


def upload_file_to_s3(s3_client: boto3.client, s3_bucket_name: str, data: dict) -> dict:
    """Upload a file to a S3 bucket.
    Parameters:
        s3_client: Object representing a session with S3
        s3_bucket_name: Name of S3 bucket to upload archive to
        data: Data to be uploaded to S3
    Returns:
        Response to the upload attempt.
    """
    try:
        filename = f"playlist_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        response = s3_client.put_object(Bucket=s3_bucket_name, Body=json.dumps(data, ensure_ascii=False), Key=filename)
    except ClientError:
        raise
    else:
        return response


def main(s3_bucket_name: str, data_to_archive: dict):
    """Main method for archiving data in S3.
    Parameters:
        s3_bucket_name: Name of S3 bucket to upload archive to
        data_to_archive: Data to archive
    """
    region = read_config("secrets.cfg", "data_lake", "region")
    s3_client = boto3.client(
        "s3",
        region_name=region,
        endpoint_url=f"http://{read_config('secrets.cfg', 'data_lake', 'host')}:{read_config('secrets.cfg', 'data_lake', 'port')}",
        aws_access_key_id=read_config("secrets.cfg", "data_lake", "aws_access_key_id"),
        aws_secret_access_key=read_config("secrets.cfg", "data_lake", "aws_secret_access_key"),
    )
    create_s3_bucket(s3_client, s3_bucket_name, region)
    upload_file_to_s3(s3_client, s3_bucket_name, data_to_archive)
