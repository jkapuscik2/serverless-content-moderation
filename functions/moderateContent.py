import json
import os
from urllib.parse import unquote_plus

import boto3

client = boto3.client('stepfunctions')


def handler(event, ctx):
    record = event["Records"][0]['s3']

    client.start_execution(
        stateMachineArn=os.environ['CONTENT_MODERATION_ARN'],
        input=json.dumps({
            "bucketName": record["bucket"]["name"],
            "objectKey": unquote_plus(record["object"]["key"])
        }),
    )
