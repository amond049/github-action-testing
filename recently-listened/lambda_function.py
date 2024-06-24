# Will need to retrieve the credentials from secrets manager
import boto3
import json
from botocore.exceptions import ClientError
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask
import awsgi

# Thinking of using a Flask application to navigate the authorization
app = Flask(__name__)


# This is the link to the Lambda https://ebc2llbzrd4v43kqzwc6ctw2cy0jqjzb.lambda-url.us-east-2.on.aws/
def lambda_handler(event, context):
    # Some additional mappings are required because they don't exist in the new version of AWS
    secret_name = 'mickeys-marvels/spotipy'
    region = 'us-east-2'
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )

    CLIENT_ID = ""
    CLIENT_SECRET = ""
    REDIRECT_URI = ""

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response['SecretString']

        CLIENT_ID = secret_string[14:46]
        CLIENT_SECRET = secret_string[65:98]
        REDIRECT_URI = secret_string[115:len(secret_string) - 2]

    except ClientError as e:
        print("Something went wrong, printing error information")
        print(e)

    event['httpMethod'] = event['requestContext']['http']['method']
    event['path'] = event['requestContext']['http']['path']
    event['queryStringParameters'] = event.get('queryStringParameters', {})
    return awsgi.response(app, event, context)

# May have to use some requests to get the authorization working
@app.route("/")
def index():
    return "This is a test"
