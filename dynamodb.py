import boto3
import botocore.exceptions

# Initialize a session using Amazon DynamoDB
session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name=''
)

# Initialize DynamoDB resource
dynamodb = session.resource('dynamodb')

def create_table():
    try:
        # Create a DynamoDB table
        table = dynamodb.create_table(
            TableName='Users',
            KeySchema=[
                {
                    'AttributeName': 'UserID',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'UserID',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table exists
        table.meta.client.get_waiter('table_exists').wait(TableName='Users')

        print(f'Table {table.table_name} is created successfully.')
    except botocore.exceptions.ClientError as e:
        print(f'An error occurred: {e.response["Error"]["Message"]}')

def insert_item():
    table = dynamodb.Table('Users')

    try:
        # Insert a new item
        table.put_item(
            Item={
                'UserID': '12345',
                'Name': 'John Doe',
                'Email': 'john.doe@example.com'
            }
        )
        print('Item inserted successfully.')
    except botocore.exceptions.ClientError as e:
        print(f'An error occurred: {e.response["Error"]["Message"]}')

def get_item():
    table = dynamodb.Table('Users')

    try:
        response = table.get_item(
            Key={
                'UserID': '12345'
            }
        )

        item = response.get('Item')
        if item:
            print(f'Item retrieved: {item}')
        else:
            print('Item not found.')
    except botocore.exceptions.ClientError as e:
        print(f'An error occurred: {e.response["Error"]["Message"]}')

def update_item():
    table = dynamodb.Table('Users')

    try:
        table.update_item(
            Key={
                'UserID': '12345'
            },
            UpdateExpression='SET Email = :email',
            ExpressionAttributeValues={
                ':email': 'new.email@example.com'
            }
        )
        print('Item updated successfully.')
    except botocore.exceptions.ClientError as e:
        print(f'An error occurred: {e.response["Error"]["Message"]}')

def delete_item():
    table = dynamodb.Table('Users')

    try:
        table.delete_item(
            Key={
                'UserID': '12345'
            }
        )
        print('Item deleted successfully.')
    except botocore.exceptions.ClientError as e:
        print(f'An error occurred: {e.response["Error"]["Message"]}')

if __name__ == '__main__':
    # create_table()
    insert_item()
    # get_item()
    # update_item()
    # get_item()  # Retrieve the updated item
    # delete_item()
    # get_item()  # Try to retrieve the deleted item
