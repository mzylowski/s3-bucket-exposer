from flask import render_template

from configuration import consts
from exposers.base import BaseExposer
from objects.s3_object import S3Object


class HTMLExposer(BaseExposer):
    def expose_list_of_buckets(self, buckets):
        return render_template("bucket_list.html",
                               buckets=buckets,
                               product_version=consts.APP_FULL_NAME)

    def expose_list_of_objects(self, bucket, objects: [S3Object]):
        return render_template("object_list.html",
                               bucket=bucket,
                               objects=objects,
                               product_version=consts.APP_FULL_NAME)
