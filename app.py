import helpers
from flask import Flask

app = Flask("s3-bucket-exposer")
provider = helpers.spawn_provider()
exposer = helpers.spawn_exposer()


@app.route("/")
def index():
    buckets = provider.list_of_buckets()
    return exposer.expose_list_of_buckets(buckets)


@app.route("/<bucket_name>")
def file_list(bucket_name):
    return exposer.expose_list_of_buckets(provider.list_of_buckets())


@app.route("/download/<bucket_name>/<file_name>")
def download_file(bucket_name, file_name):
    return "downloading file_name..."
