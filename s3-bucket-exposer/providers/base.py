import logging

from configuration.config import consts, Configuration as Config
from objects.s3_object import S3Object


class BaseProvider(object):
    def __init__(self):
        self.client = self.get_client()
        self.all_buckets_allowed = lambda: Config.get_exposer_allowed_buckets() == consts.ALL_BUCKETS_ALLOWED
        self.is_bucket_allowed = lambda x: self.all_buckets_allowed() or x in Config.get_exposer_allowed_buckets()

    def get_client(self):
        pass

    def list_of_buckets(self):
        logging.info("Getting list of available buckets.")
        response = self.client.list_buckets()
        s3_buckets = [b["Name"] for b in response.get("Buckets", [])]
        return self._intersect_allowed_buckets(s3_buckets)

    def list_of_objects(self, bucket_name):
        logging.info(f"Getting list of available objects in {bucket_name} bucket.")
        if not self.is_bucket_allowed(bucket_name):
            return None
        try:
            response = self.client.list_objects(Bucket=bucket_name).get("Contents", [])
        except self.client.exceptions.NoSuchBucket:
            return None

        return [S3Object(name=obj['Key'], date=obj['LastModified'], size=obj['Size'])
                for obj in response if float(obj['Size']) != 0]

    def generate_download_url(self, bucket, key):
        if self.is_bucket_allowed(bucket):
            logging.info(f"Generating download URL for {bucket}/{key}")
            return self.client.generate_presigned_url('get_object',
                                                      Params={'Bucket': bucket, 'Key': key},
                                                      ExpiresIn=15)
        logging.info(f"Request for download URL for object in not existing bucket ({bucket}) is aborted.")
        return None

    def _intersect_allowed_buckets(self, s3_buckets):
        return s3_buckets if self.all_buckets_allowed() else [b for b in s3_buckets if self.is_bucket_allowed(b)]
