from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>200 OK</h1>"


@app.route("/<bucket_name>")
def file_list(bucket_name):
    return "bucket_name"


@app.route("/download/<bucket_name>/<file_name>")
def download_file(bucket_name, file_name):
    return "downloading file_name..."
