import boto3
import json
import os

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')

    # Get table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    # Get item_id from path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']

    try:
        response = dynamo_client.scan(
            TableName=table_name,
            FilterExpression='item_id = :item_id',
            ExpressionAttributeValues={
                ':item_id': {'S': item_id}
            }
        )

        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found")
            }

        return {
            'statusCode': 200,
            'body': json.dumps(items[0], default=str)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }