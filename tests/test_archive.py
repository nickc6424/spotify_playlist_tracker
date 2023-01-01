from unittest.mock import patch
from scripts import archive
from botocore.exceptions import ClientError
import pytest


@patch("scripts.archive.boto3.client")
def test_create_s3_bucket_success(mock_boto3_client):
    response = {
        "ResponseMetadata": {
            "RequestId": "zqiGJxVlmpxxwKvIJUWlin6k1FVj6ybM1LYU67V0dNeNHa567QOp",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "content-type": "application/xml; charset=utf-8",
            },
            "RetryAttempts": 0,
        },
        "Location": "http://playlist-extracts.s3.localhost.localstack.cloud:4566/",
    }
    mock_boto3_client.create_bucket.return_value = response
    assert archive.create_s3_bucket(mock_boto3_client, "bucket_name", "eu-west-2") == response


@patch("scripts.archive.boto3.client")
def test_create_s3_bucket_BucketAlreadyOwnedByYou(mock_boto3_client):
    error_response = {
        "Error": {
            "Code": "BucketAlreadyOwnedByYou",
            "Message": "Your previous request to create the named bucket succeeded and you already own it.",
            "BucketName": "playlist-extracts",
        },
        "ResponseMetadata": {
            "RequestId": "d5h2JiAtlBt4gIutSlPmKivtvpiRZQYlq9PolSLFrGAieCBmRkzB",
            "HTTPStatusCode": 409,
            "HTTPHeaders": {
                "content-type": "application/xml; charset=utf-8",
            },
            "RetryAttempts": 0,
        },
    }
    mock_boto3_client.create_bucket.side_effect = ClientError(error_response, "BucketAlreadyOwnedByYou")
    assert archive.create_s3_bucket(mock_boto3_client, "bucket_name", "eu-west-2") is None


@patch("scripts.archive.boto3.client")
def test_create_s3_bucket_BucketAlreadyExists(mock_boto3_client):
    error_response = {
        "Error": {
            "Code": "BucketAlreadyExists",
            "Message": "Your previous request to create the named bucket failed because it already exists.",
            "BucketName": "playlist-extracts",
        },
        "ResponseMetadata": {
            "RequestId": "d5h2JiAtlBt4gIutSlPmKivtvpiRZQYlq9PolSLFrGAieCBmRkzB",
            "HTTPStatusCode": 409,
            "HTTPHeaders": {
                "content-type": "application/xml; charset=utf-8",
            },
            "RetryAttempts": 0,
        },
    }
    mock_boto3_client.create_bucket.side_effect = ClientError(error_response, "BucketAlreadyExists")
    assert archive.create_s3_bucket(mock_boto3_client, "bucket_name", "eu-west-2") is None


@patch("scripts.archive.boto3.client")
def test_create_s3_bucket_error(mock_boto3_client):
    error_response = {
        "Error": {
            "Code": "SomeServiceException",
            "Message": "Details/context around the exception or error",
            "BucketName": "playlist-extracts",
        },
        "ResponseMetadata": {
            "RequestId": "d5h2JiAtlBt4gIutSlPmKivtvpiRZQYlq9PolSLFrGAieCBmRkzB",
            "HTTPStatusCode": 409,
            "HTTPHeaders": {
                "content-type": "application/xml; charset=utf-8",
            },
            "RetryAttempts": 0,
        },
    }
    mock_boto3_client.create_bucket.side_effect = ClientError(error_response, "SomeServiceException")
    with pytest.raises(ClientError):
        archive.create_s3_bucket(mock_boto3_client, "bucket_name", "uk-west-2")


@patch("scripts.archive.boto3.client")
def test_upload_file_to_s3_success(mock_boto3_client):
    response = {
        "ResponseMetadata": {
            "RequestId": "KFKb6vDc6lHHEhdMRApoU0u9HGoJGWgZSM7nn4O1OCMdRGbhAbxe",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "content-type": "text/html; charset=utf-8",
            },
            "RetryAttempts": 0,
        },
        "ETag": '"a2d4e0ee4c56225edb93cd5fd87ee9a3"',
    }
    mock_boto3_client.put_object.return_value = response
    assert archive.upload_file_to_s3(mock_boto3_client, "bucket_name", {"data": "value"}) == response


@patch("scripts.archive.boto3.client")
def test_upload_file_to_s3_error(mock_boto3_client):
    error_response = {
        "Error": {
            "Code": "SomeServiceException",
            "Message": "Details/context around the exception or error",
            "BucketName": "playlist-extracts",
        },
        "ResponseMetadata": {
            "RequestId": "d5h2JiAtlBt4gIutSlPmKivtvpiRZQYlq9PolSLFrGAieCBmRkzB",
            "HTTPStatusCode": 409,
            "HTTPHeaders": {
                "content-type": "application/xml; charset=utf-8",
            },
            "RetryAttempts": 0,
        },
    }
    mock_boto3_client.put_object.side_effect = ClientError(error_response, "SomeServiceException")
    with pytest.raises(ClientError):
        archive.upload_file_to_s3(mock_boto3_client, "bucket_name", {"data": "value"})
