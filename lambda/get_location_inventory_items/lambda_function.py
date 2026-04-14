import boto3
import json
import os

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')

    # Get table and index name from environment variables
    table_name = os.getenv('TABLE_NAME', 'Inventory')
    index_name = os.getenv('LOCATION_INDEX', 'location-index')

    # Get location_id from path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    location_id = event['pathParameters']['id']

    try:
        response = dynamo_client.query(
            TableName=table_name,
            IndexName=index_name,
            KeyConditionExpression='location_id = :location_id',
            ExpressionAttributeValues={
                ':location_id': {'N': str(location_id)}
            }
        )

        items = response.get('Items', [])

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