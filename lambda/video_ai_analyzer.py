import boto3
import os
import logging
import json
import subprocess
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        if not key.endswith('.mp4') or not key.startswith('converted/'):
            logger.warning(f"Skipping unsupported file: {key}")
            continue

        # Start Rekognition Label Detection (Async)
        rekognition_response = rekognition.start_label_detection(
            Video={'S3Object': {'Bucket': bucket, 'Name': key}},
            NotificationChannel={
                'SNSTopicArn': os.environ['REKOGNITION_TOPIC_ARN'],
                'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
            }
        )

        logger.info(f"Started label detection for {key}")
        logger.info(f"Rekognition Job ID: {rekognition_response['JobId']}")

        # Download video to /tmp for FFmpeg
        tmp_path = f"/tmp/{os.path.basename(key)}"
        s3.download_file(bucket, key, tmp_path)

        # Capture thumbnail from 1st second
        thumb_path = tmp_path.replace('.mp4', '.jpg')
        subprocess.run([
            '/opt/bin/ffmpeg', '-i', tmp_path, '-ss', '00:00:01.000',
            '-vframes', '1', thumb_path
        ], check=True)

        # Upload thumbnail
        thumb_key = f"thumbnails/{os.path.basename(thumb_path)}"
        with open(thumb_path, 'rb') as img:
            s3.put_object(Bucket=bucket, Key=thumb_key, Body=img, ContentType='image/jpeg')

        # Get video metadata
        result = subprocess.run(
            ['/opt/bin/ffmpeg', '-i', tmp_path],
            stderr=subprocess.PIPE,
            text=True
        )
        metadata = result.stderr

        meta_key = f"metadata/{os.path.basename(key)}.txt"
        s3.put_object(Bucket=bucket, Key=meta_key, Body=metadata.encode('utf-8'))

        logger.info(f"Metadata and thumbnail uploaded for {key}")

    return {
        'statusCode': 200,
        'body': 'Video AI processing started successfully'
    }
