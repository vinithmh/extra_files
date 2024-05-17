import boto3
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')
size = (300, 300)

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response = s3.get_object(Bucket=bucket, Key=key)
    image = Image.open(BytesIO(response['Body'].read()))
    image.thumbnail(size)
    
    buffer = BytesIO()
    image.save(buffer, 'JPEG')
    buffer.seek(0)
    
    s3.put_object(Bucket=bucket, Key='resized/' + key, Body=buffer, ContentType='image/jpeg')

    return {
        'statusCode': 200,
        'body': 'Image resized and uploaded to ' + 'resized/' + key
    }
