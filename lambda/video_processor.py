import boto3
import os
import subprocess
from urllib.parse import unquote_plus

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        # Get bucket and key
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        # Local paths
        download_path = f"/tmp/{os.path.basename(key)}"
        output_filename = os.path.splitext(os.path.basename(key))[0] + ".mp4"
        output_path = f"/tmp/{output_filename}"
        output_s3_key = f"processed/{output_filename}"

        try:
            # Download video
            s3.download_file(bucket, key, download_path)

            # Convert to mp4
            subprocess.run(
                ["/opt/bin/ffmpeg", "-i", download_path, output_path],
                check=True
            )

            # Upload processed video
            s3.upload_file(output_path, bucket, output_s3_key)

            return {
                "statusCode": 200,
                "body": f"Processed video uploaded to {output_s3_key}"
            }

        except subprocess.CalledProcessError as e:
            return {
                "statusCode": 500,
                "error": f"FFmpeg failed: {e}"
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "error": str(e)
            }
