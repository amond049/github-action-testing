import json
import boto3


def lambda_handler(event, context):
    db = boto3.resource('dynamodb')
    table = db.Table('mickeys-marvels')

    response = table.scan(
        Select='ALL_ATTRIBUTES',
        Limit=9
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': response
    }
