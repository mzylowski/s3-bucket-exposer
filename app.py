from flask import Flask

from managers import consts
from managers.configuration import ConfigurationManager as cm
from providers import minio, aws

app = Flask("s3-bucket-exposure")


def call_provider():
    provider = cm.get_s3_provider()
    if provider == consts.MINIO_PROVIDER:
        return minio.MinioProvider()
    elif provider == consts.AWS_PROVIDER:
        return aws.AWSProvider
    else:
        raise Exception(f"Unsupported S3 provider: {provider}")


@app.route("/")
def index():
    provider = call_provider()
    return str(provider.list_of_buckets())


@app.route("/<bucket_name>")
def file_list(bucket_name):
    return "bucket_name"


@app.route("/download/<bucket_name>/<file_name>")
def download_file(bucket_name, file_name):
    return "downloading file_name..."
