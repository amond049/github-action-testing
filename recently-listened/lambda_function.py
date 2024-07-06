import json
import os
# The name of the folder in the layer MUST BE python!
import requests
from requests.auth import HTTPBasicAuth
from json import JSONEncoder

# Some global variables
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']

class TrackEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__

class Track:
    def __init__(self, track_name, album_cover_link, album_link, artists):
        self.track_name = track_name
        self.album_cover_link = album_cover_link
        self.album_link = album_link
        self.artists = artists

def get_recently_played(token):
    # This is where the most recent 20 tracks will be retrieved
    response = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played",
        params={'limit': 20},
        headers={'Authorization': 'Bearer ' + token}
    )

    response_as_json = response.json()
    tracks_list = []

    for item in response_as_json['items']:
        track_name = item['track']['name']
        album_cover_link = item['track']['album']['images'][0]['url']
        album_link = item['track']['album']['images'][0]['url']
        artists = item['track']['artists']

        new_track = Track(track_name, album_cover_link, album_link, artists)
        tracks_list.append(new_track)

    return tracks_list




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
    # Will need some sort of verification here regarding the event and endpoint is being called, can then correctly call the lambda function

    tracks = get_recently_played(new_token)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(tracks, cls=TrackEncoder)
    }
