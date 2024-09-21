import os
import boto3
import boto3.session


class S3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client
        self.client = boto3.client("s3")

    def generate_presigned_post(self, object_name, expiration=1000):
        return self.client.generate_presigned_post(
            self.bucket_name, object_name, ExpiresIn=expiration
        )
