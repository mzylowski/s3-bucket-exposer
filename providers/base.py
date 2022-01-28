from managers.configuration import consts, ConfigurationManager as Cm
from objects.s3_object import S3Object


class BaseProvider(object):
    def __init__(self):
        self.client = self.get_client()
        self.is_bucket_allowed = lambda x: x in Cm.get_exposer_allowed_buckets()

    def get_client(self):
        pass

    def list_of_buckets(self):
        response = self.client.list_buckets()
        s3_buckets = [b["Name"] for b in response.get("Buckets", [])]
        return self._intersect_allowed_buckets(s3_buckets)

    def list_of_objects(self, bucket_name):
        accessible_buckets = self.list_of_buckets()
        if bucket_name not in accessible_buckets:
            return None
        response = self.client.list_objects(Bucket=bucket_name).get("Contents", [])
        return [S3Object(name=obj['Key'], date=obj['LastModified'], size=obj['Size']) for obj in response]

    def _intersect_allowed_buckets(self, s3_buckets):
        return s3_buckets if Cm.get_exposer_allowed_buckets() == consts.ALL_BUCKETS_ALLOWED else \
            [bucket for bucket in s3_buckets if self.is_bucket_allowed(bucket)]
