# Will need to retrieve the credentials from secrets manager
import boto3
import json
from botocore.exceptions import ClientError
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect
import awsgi

# Thinking of using a Flask application to navigate the authorization
app = Flask(__name__)

# Setting it to None for the time being
sp = None

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = ""

scope = "user-read-recently-played"

secret_name = 'mickeys-marvels/spotipy'
region = 'us-east-2'
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=region
)

try:
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response['SecretString']

    CLIENT_ID = secret_string[14:46]
    CLIENT_SECRET = secret_string[65:98]
    REDIRECT_URI = secret_string[115:len(secret_string) - 2]

except ClientError as e:
    print("Something went wrong, printing error information")
    print(e)

def lambda_handler(event, context):
    # Some additional mappings are required because they don't exist in the new version of AWS
    event['httpMethod'] = event['requestContext']['http']['method']
    event['path'] = event['requestContext']['http']['path']
    event['queryStringParameters'] = event.get('queryStringParameters', {})
    return awsgi.response(app, event, context)


# May have to use some requests to get the authorization working
@app.route("/")
def index():
    auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=scope, redirect_uri=REDIRECT_URI)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    return redirect(auth_manager.get_authorize_url())

@app.route("/callback")
def callback():
    return "Let's see if this works"