from exposers.base import BaseExposer
from objects.s3_object import S3Object


class HTMLExposer(BaseExposer):
    def expose_list_of_buckets(self, buckets):
        return "</br>".join(buckets)

    def expose_list_of_objects(self, objects: [S3Object]):
        code = ""
        for obj in objects:
            code += f"{obj.name}</br>"
        return code
