import os
import boto3
import boto3.session


class S3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client
        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

    def generate_presigned_url(self, object_name, expiration=3600, http_method="PUT"):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/generate_presigned_url.html
        return self.client.generate_presigned_url(
            "put_object",
            Params={"Bucket": self.bucket_name, "Key": object_name},
            ExpiresIn=expiration,
            HttpMethod=http_method,
        )
