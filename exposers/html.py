from exposers.base import BaseExposer


class HTMLExposer(BaseExposer):
    def expose_list_of_buckets(self, buckets):
        return "</br>".join(buckets)
