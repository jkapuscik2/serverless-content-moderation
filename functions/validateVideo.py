import json
import os
import time

import boto3

from validation import has_unsafe_label

MIN_CONFIDENCE = 75
rekognition = boto3.client('rekognition')
sqs = boto3.client('sqs')
sns = boto3.client('sns')


def handler(event, ctx):
    response = rekognition.start_content_moderation(
        Video={
            'S3Object':
                {
                    'Bucket': event["bucketName"],
                    'Name': event["objectKey"]
                }
        },
        NotificationChannel={
            'RoleArn': os.environ['ROLE_ARN'],
            'SNSTopicArn': os.environ['TOPIC_ARN'],
        }
    )
    labels = get_labels(response['JobId'])

    return {
        "isUnsafe": has_unsafe_label(labels),
        "labels": labels,
        "content": {
            "bucketName": event["bucketName"],
            "objectKey": event["objectKey"],
            "mime": event["mime"]
        }
    }


STATUS_SUCCESS = "SUCCEEDED"
STATUS_FAILED = "FAILED"


def get_labels(job_id):
    sqs_url = os.environ['MODERATION_QUEUE_URL']

    while True:
        sqs_response = sqs.receive_message(
            QueueUrl=sqs_url,
            MessageAttributeNames=['ALL'],
            MaxNumberOfMessages=10
        )
        if sqs_response:
            if 'Messages' not in sqs_response:
                time.sleep(1)
                continue

            for message in sqs_response['Messages']:
                notification = json.loads(message['Body'])
                content = json.loads(notification['Message'])

                if content['JobId'] == job_id:
                    if content['Status'] == STATUS_SUCCESS:
                        sqs.delete_message(
                            QueueUrl=sqs_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
                        return get_results(job_id)

                    if content["Status"] == STATUS_FAILED:
                        sqs.delete_message(
                            QueueUrl=sqs_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
                        raise Exception('Video moderation failed')


def get_results(job_id):
    max_results = 100
    pagination_token = ''
    finished = False
    labels = []

    while not finished:
        response = rekognition.get_content_moderation(
            JobId=job_id,
            MaxResults=max_results,
            NextToken=pagination_token
        )
        for label in response['ModerationLabels']:
            labels.append(label["ModerationLabel"])

        if 'NextToken' in response:
            pagination_token = response['NextToken']
        else:
            finished = True

    return labels
