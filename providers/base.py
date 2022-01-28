from managers.configuration import consts, ConfigurationManager as Cm
from objects.s3_object import S3Object


class BaseProvider(object):
    def __init__(self):
        self.client = self.get_client()
        self.all_buckets_allowed = lambda: Cm.get_exposer_allowed_buckets() == consts.ALL_BUCKETS_ALLOWED
        self.is_bucket_allowed = lambda x: self.all_buckets_allowed or x in Cm.get_exposer_allowed_buckets()

    def get_client(self):
        pass

    def list_of_buckets(self):
        response = self.client.list_buckets()
        s3_buckets = [b["Name"] for b in response.get("Buckets", [])]
        return self._intersect_allowed_buckets(s3_buckets)

    def list_of_objects(self, bucket_name):
        if not self.is_bucket_allowed(bucket_name):
            return None
        response = self.client.list_objects(Bucket=bucket_name).get("Contents", [])
        return [S3Object(name=obj['Key'], date=obj['LastModified'], size=obj['Size']) for obj in response]

    def generate_download_url(self, bucket, key):
        if self.is_bucket_allowed(bucket):
            return self.client.generate_presigned_url('get_object',
                                                      Params={'Bucket': bucket, 'Key': key},
                                                      ExpiresIn=15)
        return None

    def _intersect_allowed_buckets(self, s3_buckets):
        return s3_buckets if self.all_buckets_allowed else [b for b in s3_buckets if self.is_bucket_allowed(b)]
