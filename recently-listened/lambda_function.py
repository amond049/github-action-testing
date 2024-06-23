# Will need to retrieve the credentials from secrets manager
import boto3
import json
from botocore.exceptions import ClientError
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# from spotipy.oauth2 import SpotifyClientCredentials


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

    secrets_as_string = get_response['SecretString']
    split_secrets = secrets_as_string.split(",")
    client_id = ""
    client_secret = ""
    redirect_uri = ""

    for string in split_secrets:
        each_string = string.split(":")
        if each_string[0] == '{"CLIENT_ID"':
            client_id = each_string[1]
        elif each_string[0] == '"CLIENT_SECRET"':
            client_secret = each_string[1]
        elif each_string[0] == '"REDIRECT_URI"':
            combined_url = each_string[1] + each_string[2] + each_string[3]
            # Requires some further processing unfortunately
            redirect_uri = combined_url.split("}")[0]

    CLIENT_ID = client_id
    CLIENT_SECRET = client_secret
    REDIRECT_URI = redirect_uri

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope="user-read-recently-played",
                                                   open_browser=False))

    result = sp.current_user_recently_played(limit=20)

    print(result)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda! This is the second one')
    }

'''
def main():
    id = "3646292c293e4267bb6c48ab048d6a0c"
    secret = "91bf3b806b744a0ebefe82ecb3229c74"
    uri = "http://localhost:1234/"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id,
                                                   client_secret=secret,
                                                   redirect_uri=uri,
                                                   scope="user-read-recently-played",
                                                   open_browser=False))

    result = sp.current_user_recently_played(limit=20)

    print(result)

main()
'''
