import boto3
import json
import os

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')

    # Get table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    # Extract item_id from path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']

    try:
        # First find the item using scan
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

        # Get location_id from found item
        location_id = items[0]['location_id']['N']

        # Delete using both PK and SK
        dynamo_client.delete_item(
            TableName=table_name,
            Key={
                'item_id': {'S': item_id},
                'location_id': {'N': location_id}
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {item_id} deleted successfully.")
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }