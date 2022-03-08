from flask import abort, redirect as flask_redirect

from objects.s3_object import S3Object


# BaseExposer class is also implementation of empty exposer
class BaseExposer(object):
    def expose_list_of_buckets(self, buckets):
        return ""

    def expose_list_of_objects(self, bucket, objects: [S3Object]):
        return ""

    def redirect(self, url):
        if url:
            return flask_redirect(url)
        return abort(404)
