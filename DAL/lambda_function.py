import json
import boto3

def lambda_handler(event, context):
    db = boto3.resource('dynamodb')

    table = db.Table('mickeys-marvels')

    response = table.get_item(
        Key={
            'entryID': 0
        }
    )

    print(response['Item'])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda and Github Actions with the Lambda working as intended!')
    }
