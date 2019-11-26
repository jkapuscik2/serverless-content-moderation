import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')


def handler(event, ctx):
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    table.put_item(
        Item={
            'BucketName': event['content']["bucketName"],
            'ObjectKey': event['content']["objectKey"],
            "Mime": event["content"]["mime"],
            'Labels': json.dumps(event['labels']),
            'IsUnsafe': event['isUnsafe']
        }
    )
