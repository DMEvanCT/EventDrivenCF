import json
import boto3

# import requests


def lambda_handler(event, context):
  # Put event into event bridge with source laji_project.policydata
    events = boto3.client('events')
    response = events.put_events(
        Entries=[
            {
                'Source': 'laji_project.policydata',
                'DetailType': 'policydata',
                'Detail': json.dumps(event["body"]),
                'EventBusName': 'PolicyEventBus'
            },
        ]
    )

    return {
            "statusCode": 200,
            "body": json.dumps({
            "Status": "Policy Submited",
            "DataSent": json.dumps(event["body"]),
            "PolicyData": json.dumps(event["body"]["policyType"])
        }),
    }

