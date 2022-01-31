import boto3

from providers.base import BaseProvider


class AWSProvider(BaseProvider):
    def get_client(self):
        raise NotImplementedError
        # client: boto3.resource('s3') = boto3.client(
        #     's3',
        #     #aws_access_key_id=YOUR_AWS_ACCESS_KEY,
        #     #aws_secret_access_key=YOUR_AWS_SECRET_KEY
        # )
