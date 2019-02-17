import json
from flask import Flask, redirect, render_template, request

import logging
import os

from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision

import backtest as nl

CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')
PREFIX = 'gs://anteat/'
session = {}

app = Flask(__name__)


@app.route('/')
def homepage():
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Use the Cloud Datastore client to fetch information from Datastore about
    # each photo.
    query = datastore_client.query(kind='Audio clips')
    audio_entities = list(query.fetch())

    # Return a Jinja2 HTML template and pass in image_entities as a parameter.
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    audio = request.files['file']
    session['file'] = audio.filename

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

    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # The kind for the new entity.
    kind = 'Audio clips'

    # The name/ID for the new entity.
    name = blob.name

    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, name)

    # Construct the new entity using the key. Set dictionary values for entity
    # keys blob_name, storage_public_url, timestamp, and joy.
    entity = datastore.Entity(key)
    entity['blob_name'] = blob.name
    entity['audio_public_url'] = blob.public_url
    session['public_url'] = blob.public_url
    # Save the new entity to Datastore.
    datastore_client.put(entity)

    # Redirect to the home page.
    return redirect('/process')

@app.route('/process')
def process():
    filename = PREFIX + session.get('file', None)
    wordTimeMap, keywords = nl.returnWordTimeAndKeyWord(filename)

    audio_url = session.get('public_url', None)
    name = session.get('file', None)
    # Return a Jinja2 HTML template and pass in image_entities as a parameter.
    return render_template('/output.html', audio_url=audio_url, keywords=keywords, wordTimeMap=wordTimeMap, name=name)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
