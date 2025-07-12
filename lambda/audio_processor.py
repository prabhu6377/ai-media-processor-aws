import os
import subprocess
import boto3
import urllib.parse

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        # 1. Get bucket and file info
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        if not key.endswith('.wav'):
            continue  # Skip non-WAV files

        filename = key.split('/')[-1]
        base_filename = filename.rsplit('.', 1)[0]

        # 2. Download from S3
        input_path = f"/tmp/{filename}"
        output_path = f"/tmp/{base_filename}.mp3"

        s3.download_file(bucket, key, input_path)

        # 3. Convert using FFmpeg
        try:
            result = subprocess.run(
                ["/opt/bin/ffmpeg", "-y", "-i", input_path, output_path],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise Exception(result.stderr)

        except Exception as e:
            return {
                "statusCode": 500,
                "error": f"FFmpeg error: {str(e)}"
            }

        # 4. Upload back to S3
        output_key = key.replace("input/", "output/").replace(".wav", ".mp3")
        s3.upload_file(output_path, bucket, output_key)

    return {
        "statusCode": 200,
        "message": "Audio processed successfully"
    }
