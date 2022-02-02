import boto3

from configuration.config import Configuration
from providers.base import BaseProvider


class MinioProvider(BaseProvider):
    def get_client(self):
        return boto3.client('s3',
                            endpoint_url=Configuration.get_minio_endpoint(),
                            aws_access_key_id=Configuration.get_s3_access_key(),
                            aws_secret_access_key=Configuration.get_s3_secret_key(),
                            config=boto3.session.Config(
                                signature_version='s3v4'))
