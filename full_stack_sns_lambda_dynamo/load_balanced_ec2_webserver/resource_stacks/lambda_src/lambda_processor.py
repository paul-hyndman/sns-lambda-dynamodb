import json
import logging
import os
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    logging.getLogger().setLevel(level=os.getenv('LOG_LEVEL', 'DEBUG').upper())
    table_name = os.getenv('table_name')
    
    message = event['Records'][0]['Sns']['Message']
    
    parsed_message = json.loads(message)
    orderId = parsed_message["orderId"]
    customerId = parsed_message["customerId"]
    sku = parsed_message["sku"]
    quantity = parsed_message["quantity"]
    
    client.put_item(
        TableName=table_name,
        Item={
            'order_id': {
            'S': orderId
            },
            'customer_id': {
            'S': customerId
            },
            'sku': {
            'S': sku
            },
            'quantity': {
            'S': str(quantity)
            }
        }
    )    
    
    return {
        "statusCode:": 200,
        "body": json.dumps({
            "message": parsed_message
        })
    }