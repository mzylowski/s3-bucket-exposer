from flask import Flask

import helpers
from exposers.base import BaseExposer

app = Flask("s3-bucket-exposer")
provider = helpers.spawn_provider()
exposer = helpers.spawn_exposer()


@app.route("/")
def index():
    if type(exposer) == BaseExposer:
        return ""
    return exposer.expose_list_of_buckets(provider.list_of_buckets())


@app.route("/<bucket_name>")
def file_list(bucket_name):
    if type(exposer) == BaseExposer:
        return ""
    return exposer.expose_list_of_objects(provider.list_of_objects(bucket_name))


@app.route("/download/<bucket_name>/<file_name>")
def download_file(bucket_name, file_name):
    return exposer.redirect(provider.generate_download_url(bucket_name, file_name))
