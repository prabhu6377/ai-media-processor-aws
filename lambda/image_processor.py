import boto3
from PIL import Image, UnidentifiedImageError
import io
import logging
import json
import os
from urllib.parse import unquote_plus

# Clients
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

# Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            image_data = response['Body'].read()

            # Try to open the image using PIL
            img = Image.open(io.BytesIO(image_data))
            img.thumbnail((128, 128))

            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            buffer.seek(0)

            # Save resized image
            output_key = f"processed/{key.rsplit('.', 1)[0]}.jpg"
            s3.put_object(
                Bucket=bucket,
                Key=output_key,
                Body=buffer,
                ContentType='image/jpeg'
            )
            logger.info(f"Processed image: {key}")

            # === AI LABEL DETECTION ===
            rekog_response = rekognition.detect_labels(
                Image={'S3Object': {'Bucket': bucket, 'Name': key}},
                MaxLabels=10,
                MinConfidence=75
            )

            label_data = {
                'Image': key,
                'Labels': rekog_response['Labels']
            }

            label_output_key = f"labels/{os.path.basename(key)}.json"
            s3.put_object(
                Bucket=bucket,
                Key=label_output_key,
                Body=json.dumps(label_data, indent=2),
                ContentType='application/json'
            )

            logger.info(f"Saved label data: {label_output_key}")

        except UnidentifiedImageError:
            logger.warning(f"Unsupported image format for file: {key}")
            s3.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': key},
                Key=f"unsupported/{key}"
            )
            s3.delete_object(Bucket=bucket, Key=key)

        except Exception as e:
            logger.error(f"Error processing {key}: {str(e)}")

    return {
        'statusCode': 200,
        'body': 'Image processing and labeling completed.'
    }
