import boto3
import logging

from configuration.config import Configuration
from providers.base import BaseProvider


class AWSProvider(BaseProvider):
    def get_client(self, region=None):
        if region:
            return boto3.client('s3',
                                region_name=region, endpoint_url=f'https://s3.{region}.amazonaws.com',
                                aws_access_key_id=Configuration.get_s3_access_key(),
                                aws_secret_access_key=Configuration.get_s3_secret_key(),
                                config=boto3.session.Config(
                                    signature_version='s3v4'))
        else:
            return boto3.client('s3',
                                aws_access_key_id=Configuration.get_s3_access_key(),
                                aws_secret_access_key=Configuration.get_s3_secret_key(),
                                config=boto3.session.Config(
                                    signature_version='s3v4'))

    def generate_download_url(self, bucket, key):
        if self.is_bucket_allowed(bucket):
            logging.info(f"Generating download URL for {bucket}/{key}")
            bucket_location = self.client.get_bucket_location(Bucket=bucket)
            regionalized_client = self.get_client(bucket_location["LocationConstraint"])
            return regionalized_client.generate_presigned_url('get_object',
                                                              Params={'Bucket': bucket, 'Key': key},
                                                              ExpiresIn=15)
        logging.info(f"Request for download URL for object in not existing bucket ({bucket}) is aborted.")
        return None
