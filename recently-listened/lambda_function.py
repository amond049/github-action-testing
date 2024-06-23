# Will need to retrieve the credentials from secrets manager
import boto3
import json
from botocore.exceptions import ClientError
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# This is the link to the Lambda https://ebc2llbzrd4v43kqzwc6ctw2cy0jqjzb.lambda-url.us-east-2.on.aws/
def lambda_handler(event, context):
    secret_name = "mickeys-marvels/spotipy"
    region = "us-east-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )

    try:
        get_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    CLIENT_ID = get_response['SecretString']['CLIENT_ID']
    CLIENT_SECRET = get_response['SecretString']['CLIENT_SECRET']
    REDIRECT_URI = get_response['SecretString']['REDIRECT_URI']

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope="user-read-recently-played"))

    result = sp.current_user_recently_played(limit = 20)

    print(result)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda! This is the second one')
    }
