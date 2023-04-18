import json
import boto3


# import requests


def lambda_handler(event, context):
    # Put event into event bridge with source laji_project.policydata
    events = boto3.client('events')
    body = json.loads(event["body"])
    response = events.put_events(
        Entries=[
            {
                'Source': 'laji_project.policydata',
                'DetailType': 'PolicyCreated',
                'Detail': json.dumps(body),
                'EventBusName': 'PolicyEventBus'
            },
        ]
    )
    print(event["body"])
    print(response)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "Status": "Policy Submited",
            "DataSent": body
        }),
    }


