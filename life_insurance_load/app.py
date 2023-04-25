import json
import os

import boto3

def lambda_handler(event, context):
    # Get items from sqs in batch of 10
    sqs = boto3.client('sqs')
    queue_url = os.getenv('SQS_QUEUE')
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
    # put items into dynamodb
    dynamodb = boto3.client('dynamodb')
    if 'Messages' in sqs_message:
        for message in sqs_message['Messages']:
            message_body = message['Body']
            message_parsed = json.loads(message_body)
            dynamodb.put_item(
                TableName='PolicyData',
                Item={
                    'PolicyNumber': {'S': message_parsed['PolicyNumber']},
                    'PolicyData': {'S': message_body}
                }
            )
            # Delete the message from the queue
            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )





