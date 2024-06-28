import json
import os
# The name of the folder in the layer MUST BE python!
import requests
from requests.auth import HTTPBasicAuth

# Some global variables
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']


def get_recently_played(token):
    # This is where the most recent 20 tracks will be retrieved
    response = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played",
        params={'limit': 20},
        headers={'Authorization': 'Bearer ' + token}
    )

    return response


def refresh_token():
    # This is where the token refreshing functionality will go
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        params={'grant_type': 'refresh_token', 'refresh_token': REFRESH_TOKEN},
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    return response.json()["access_token"]


def lambda_handler(event, context):
    new_token = refresh_token()
    tracks = get_recently_played(new_token)
    return {
        'statusCode': 200,
        'body': json.dumps(tracks.json())
    }
