import json
import requests
import boto3
import os

def get_secret(secret_name):
    client = boto3.client("secretsmanager")
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])
        return secret["api_key"]
    except Exception as e:
        raise Exception(f"Error retrieving secret: {str(e)}")

def handler(event, context):
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM/stream"  # Default voice ID
    api_key = get_secret(os.environ["SECRET_NAME"])
    headers = {"xi-api-key": api_key}
    payload = {"text": "Hello from AWS Lambda! Testing ElevenLabs voice clip."}
    response = requests.post(url, json=payload, headers=headers, stream=True)
    s3 = boto3.client("s3")
    bucket_name = os.environ["BUCKET_NAME"]
    s3.put_object(Bucket=bucket_name, Key="output.mp3", Body=response.content)
    return {"statusCode": 200, "body": json.dumps("Voice clip generated and stored in S3!")}