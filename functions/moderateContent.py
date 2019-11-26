import json
import os

import boto3

client = boto3.client('stepfunctions')


def handler(event, ctx):
    record = event["Records"][0]['s3']

    client.start_execution(
        stateMachineArn=os.environ['CONTENT_MODERATION_ARN'],
        input=json.dumps({
            "bucketName": record["bucket"]["name"],
            "objectKey": record["object"]["key"]
        }),
    )
