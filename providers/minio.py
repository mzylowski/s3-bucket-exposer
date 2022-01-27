import boto3

from managers.configuration import ConfigurationManager as cm
from providers.base import BaseProvider


class MinioProvider(BaseProvider):
    def get_client(self):
        return boto3.client('s3',
                            endpoint_url=cm.get_minio_endpoint(),
                            aws_access_key_id=cm.get_s3_access_key(),
                            aws_secret_access_key=cm.get_s3_secret_key(),
                            config=boto3.session.Config(
                                signature_version='s3v4'))
