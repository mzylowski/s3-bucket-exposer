from managers.configuration import consts, ConfigurationManager as Cm


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

    def _intersect_allowed_buckets(self, s3_buckets):
        return s3_buckets if Cm.get_exposer_allowed_buckets() == consts.ALL_BUCKETS_ALLOWED else \
            [bucket for bucket in s3_buckets if self.is_bucket_allowed(bucket)]
