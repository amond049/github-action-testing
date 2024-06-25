# Will need to retrieve the credentials from secrets manager
import boto3
import json
from botocore.exceptions import ClientError
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, request
import awsgi

# Thinking of using a Flask application to navigate the authorization
app = Flask(__name__)

# Setting it to None for the time being
sp = None


# ProductiOn Development 
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
    CLIENT_SECRET = secret_string[65:97]
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


auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=scope, redirect_uri=REDIRECT_URI)
@app.route("/")
def index():
    return redirect(auth_manager.get_authorize_url())

@app.route("/callback")
def callback():
    token = auth_manager.get_access_token(request.args.get("code"), as_dict=False)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    result = sp.current_user_recently_played(limit=20)
    return "<p>This is the token" + token + str(result) + "</p>"