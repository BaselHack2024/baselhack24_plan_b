

import boto3

# Replace these values with your local S3 service credentials and settings
local_s3_endpoint = "s3://192.168.20.250:4566"  # or Docker IP and port if different
aws_access_key_id = ""  # your local service access key
aws_secret_access_key = ""  # your local service secret key
bucket_name = "abc"  # specify the bucket you're working with

# Create a session and connect to the local S3-compatible service
client = boto3.client(
        service_name='s3',
        aws_access_key_id='abc',
        aws_secret_access_key='abc',
        endpoint_url='http://192.168.20.250:4566'
)

bucket = '01a3544b-6303-4ef2-9d14-266e55dae940'


''' client.create_bucket(Bucket=bucket) '''

''' with open('../../../assets/coffee/1.jpg', 'rb') as file:
    client.put_object(Bucket=bucket_name, Body=file, Key='picture_1.jpg') '''

print(client.list_objects_v2(Bucket=bucket))
''' for element in client.list_objects_v2(Bucket=bucket):
    print(element["Contents"]) '''


''' client.put_object(Bucket=bucket, Key=key, Body=body)
list_objects = client.list_objects_v2(Bucket=bucket) '''
