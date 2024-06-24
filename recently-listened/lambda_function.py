# Will need to retrieve the credentials from secrets manager
import boto3
import json
from botocore.exceptions import ClientError
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask
from flask import jsonify
import awsgi



# Thinking of using a Flask application to navigate the authorization
app = Flask(__name__)


# This is the link to the Lambda https://ebc2llbzrd4v43kqzwc6ctw2cy0jqjzb.lambda-url.us-east-2.on.aws/
def lambda_handler(event, context):
    return awsgi.response(app, event, context)

# May have to use some requests to get the authorization working
@app.route("/")
def index():
    return jsonify(status=200, message='Hello from Flask app in Lambda!')

