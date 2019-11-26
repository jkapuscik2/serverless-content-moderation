import json
import logging

import boto3

from updateMetadata import update_metadata

MIN_CONFIDENCE = 75
REJECTED_CATEGORIES = [
    "Explicit Nudity",
    "Violence",
    "Visually Disturbing"
]
rekognition = boto3.client('rekognition')


def has_unsafe_label(labels):
    logging.info(labels)
    for label in labels:
        if label["Name"] in REJECTED_CATEGORIES:
            return True
    return False


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
