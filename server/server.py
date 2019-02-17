
import logging
import os

from flask import Flask, redirect, render_template, request

from google.cloud import datastore
from google.cloud import storage

CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')

app = Flask(__name__, static_folder="../build/static", template_folder="../build")

@app.route("/")
def index():
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload():
    audio = request.files['file']

    # Create a Cloud Storage client.
    storage_client = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(audio.filename)
    blob.upload_from_string(
            audio.read(), content_type=audio.content_type)

    # Make the blob publicly viewable.
    blob.make_public()


if __name__ == "__main__":
    app.run(host='127.0.0.1', port='8001')
