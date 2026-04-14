import boto3
import json
import os

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')

    # Get table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    # Scan the table
    try:
        response = dynamo_client.scan(TableName=table_name)
        items = response['Items']

        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }