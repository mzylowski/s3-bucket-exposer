from exposers.base import BaseExposer


class JSONExposer(BaseExposer):
    def expose_list_of_buckets(self, buckets):
        return NotImplementedError
