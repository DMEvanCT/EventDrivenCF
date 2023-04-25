import json
import os

import boto3

# import requests


def lambda_handler(event, context):
    queue_url = os.getenv('SQS_QUEUE')
    # Create SQS client
    sqs = boto3.client('sqs')
    # Create DynamoDB client
    dynamodb = boto3.client('dynamodb')
    # Get item from queue
    sqs_message = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=15,
        WaitTimeSeconds=10
    )

    if 'Messages' in sqs_message:
        message = sqs_message['Messages'][0]
        message_body = message['Body']

        message_parsed = json.loads(message_body)

        # Delete the message from the queue
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

    else:
        print("No messages received.")
        return None

