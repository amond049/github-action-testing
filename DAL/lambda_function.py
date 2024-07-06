import json
import boto3

class EntryEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__

class Entry:
    def __init__(self, name, rating, comments, cover):
        self.name = name
        self.rating = rating
        self.comments = comments
        self.cover = cover


def lambda_handler(event, context):
    db = boto3.resource('dynamodb')
    table = db.Table('mickeys-marvels')

    response = table.scan(
        AttributesToGet=['albumName', 'rating', 'comments', 'albumCover'],
        Limit=9
    )

    entry_list = []

    for item in response['Items']:
        name = item['albumName']
        rating = item['rating']
        comments = item['comments']
        cover = item['albumCover']

        entry = Entry(name, rating, comments, cover)
        entry_list.append(entry)


    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(entry_list, cls=EntryEncoder)
    }