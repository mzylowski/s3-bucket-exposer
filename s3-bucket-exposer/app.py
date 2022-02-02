from flask import Flask

import helpers
from exposers.base import BaseExposer
from configuration.consts import APP_NAME

application = Flask(APP_NAME)
provider, exposer = helpers.initialize()


@application.route("/")
def index():
    if type(exposer) == BaseExposer:
        return ""
    return exposer.expose_list_of_buckets(provider.list_of_buckets())


@application.route("/bucket/<bucket_name>")
def file_list(bucket_name):
    if type(exposer) == BaseExposer:
        return ""
    return exposer.expose_list_of_objects(provider.list_of_objects(bucket_name))


@application.route("/download/<bucket_name>/<file_name>")
def download_file(bucket_name, file_name):
    return exposer.redirect(provider.generate_download_url(bucket_name, file_name))


if __name__ == "__main__":
    application.run()
