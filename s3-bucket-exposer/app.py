from flask import Flask

import helpers
from exposers.base import BaseExposer
from configuration.consts import APP_NAME

application = Flask(APP_NAME)
provider, exposer = helpers.initialize()


@application.route("/")
def index():
    return "" if type(exposer) == BaseExposer else exposer.expose_list_of_buckets(provider.list_of_buckets())


@application.route("/bucket/<bucket_name>")
def file_list(bucket_name):
    return "" if type(exposer) == BaseExposer else \
        exposer.expose_list_of_objects(
            bucket_name,
            provider.list_of_objects(bucket_name))


@application.route("/download/<bucket_name>/<path:rest>")
def download_file(bucket_name, rest):
    return exposer.redirect(provider.generate_download_url(bucket_name, rest))


if __name__ == "__main__":
    application.run()
