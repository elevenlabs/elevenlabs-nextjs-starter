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
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB/stream"  # Adam voice ID
    api_key = get_secret(os.environ["SECRET_NAME"])
    headers = {"xi-api-key": api_key}
    payload = {"text": "Hey ElevenLabs — first off, I absolutely love your software. I’ve been using it for years, and it’s incredible. Secondly, I just built a secure AWS Lambda deployment for your text-to-speech API, showing off some cloud security and automation magic. I’m making the leap from politics — yeah, soul-crushing, I know, I should’ve seen it coming — into IT, and I’d love to bring my skills to your team. You can check out my portfolio at T-R-I-S-O-N-C-L-O-U-D-R-E-S-U-M-E dot com. Fingers crossed you’re looking for entry-level talent. And if you’re not hiring, I’d be so grateful if you could point me toward any IT firms that might be interested in someone with my skill set — I don’t have many connections in the industry yet, and I’m just looking for a chance to get my foot in the door. Thanks so much! P.S. — the voice talking to you right now? That’s coming from the secure AWS Lambda deployment I built for your text-to-speech API."}
    response = requests.post(url, json=payload, headers=headers, stream=True)
    if response.status_code != 200:
        raise Exception(f"ElevenLabs API error: {response.status_code} - {response.text}")
    s3 = boto3.client("s3")
    bucket_name = os.environ["BUCKET_NAME"]
    s3.put_object(Bucket=bucket_name, Key="output.mp3", Body=response.content)
    return {"statusCode": 200, "body": json.dumps("Voice clip generated and stored in S3!")}