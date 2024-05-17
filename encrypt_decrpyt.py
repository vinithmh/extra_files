import boto3
from botocore.exceptions import ClientError

# AWS credentials
aws_access_key_id = ''
aws_secret_access_key = ''
region_name = ''

# Initialize S3 and KMS clients
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
kms = boto3.client('kms', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

def upload_and_encrypt_key(bucket_name, key_name, plaintext_key):
    # Upload plaintext key to S3
    s3.put_object(Bucket=bucket_name, Key=key_name, Body=plaintext_key)

    # Encrypt the key using KMS
    response = kms.encrypt(KeyId='alias/YOUR_CMK_ALIAS', Plaintext=plaintext_key)
    encrypted_key = response['CiphertextBlob']

    return encrypted_key

def decrypt_key(encrypted_key):
    # Decrypt the key using KMS
    response = kms.decrypt(CiphertextBlob=encrypted_key)
    decrypted_key = response['Plaintext']

    return decrypted_key

# Example usage
bucket_name = 'YOUR_BUCKET_NAME'
key_name = 'example_key.txt'
plaintext_key = b'YOUR_SECRET_KEY'

# Upload and encrypt the key
encrypted_key = upload_and_encrypt_key(bucket_name, key_name, plaintext_key)
print("Uploaded and encrypted key:", encrypted_key)

# Decrypt the key
decrypted_key = decrypt_key(encrypted_key)
print("Decrypted key:", decrypted_key)
