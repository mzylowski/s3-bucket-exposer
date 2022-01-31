from flask import Flask

import helpers
from exposers.base import BaseExposer
from managers.consts import APP_NAME

app = Flask(APP_NAME)
provider, exposer = helpers.initialize()


@app.route("/")
def index():
    if type(exposer) == BaseExposer:
        return ""
    return exposer.expose_list_of_buckets(provider.list_of_buckets())


@app.route("/bucket/<bucket_name>")
def file_list(bucket_name):
    if type(exposer) == BaseExposer:
        return ""
    return exposer.expose_list_of_objects(provider.list_of_objects(bucket_name))


@app.route("/download/<bucket_name>/<file_name>")
def download_file(bucket_name, file_name):
    return exposer.redirect(provider.generate_download_url(bucket_name, file_name))
