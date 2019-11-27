import json

import boto3

from updateMetadata import update_metadata
from validation import has_unsafe_label

MIN_CONFIDENCE = 75
rekognition = boto3.client('rekognition')


def handler(event, ctx):
    response = rekognition.detect_moderation_labels(
        Image={
            'S3Object': {
                'Bucket': event["bucketName"],
                'Name': event["objectKey"]
            }
        },
        MinConfidence=MIN_CONFIDENCE
    )

    update_metadata(event["bucketName"],
                    event["objectKey"],
                    {"moderation_labels": json.dumps(response["ModerationLabels"])})

    return {
        "isUnsafe": has_unsafe_label(response["ModerationLabels"]),
        "labels": response["ModerationLabels"],
        "content": {
            "bucketName": event["bucketName"],
            "objectKey": event["objectKey"],
            "mime": event["mime"]
        }
    }
