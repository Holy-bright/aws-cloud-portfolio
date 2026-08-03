import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

# Initialise outside handler for warm start performance
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Configuration — update these values
PROCESSED_BUCKET = 'bright-processed'
DYNAMODB_TABLE = 'ProcessingLog'
SNS_TOPIC_ARN = 'arn:aws:sns:image-processing-alerts'

def lambda_handler(event, context):
    print(f"Event received: {json.dumps(event)}")

    results = []

    for record in event['Records']:
        try:
            source_bucket = record['s3']['bucket']['name']
            file_key = record['s3']['object']['key']
            file_size = record['s3']['object']['size']
            event_time = record['eventTime']

            print(f"Processing: {file_key} from {source_bucket}")
            print(f"Size: {file_size} bytes")

            # Step 1: Copy file to processed bucket
            copy_source = {'Bucket': source_bucket, 'Key': file_key}

            s3.copy_object(
                CopySource=copy_source,
                Bucket=PROCESSED_BUCKET,
                Key=f"processed/{file_key}",
                MetadataDirective='COPY'
            )

            print(f"Copied to {PROCESSED_BUCKET}/processed/{file_key}")

            # Step 2: Write log to DynamoDB
            table = dynamodb.Table(DYNAMODB_TABLE)
            timestamp = datetime.now().isoformat()

            table.put_item(
                Item={
                    'filename': file_key,
                    'timestamp': timestamp,
                    'source_bucket': source_bucket,
                    'processed_bucket': PROCESSED_BUCKET,
                    'size': str(file_size),
                    'status': 'processed',
                    'event_time': event_time
                }
            )

            print(f"Logged to DynamoDB: {file_key}")

            # Step 3: Send SNS notification
            message = (
                f"Image Processing Complete\n\n"
                f"File:      {file_key}\n"
                f"Size:      {file_size:,} bytes\n"
                f"Source:    {source_bucket}\n"
                f"Processed: {PROCESSED_BUCKET}/processed/{file_key}\n"
                f"Time:      {timestamp}\n"
                f"Status:    SUCCESS"
            )

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=f"Image Processed: {file_key}",
                Message=message
            )

            print("SNS notification sent")

            results.append({
                'file': file_key,
                'status': 'success'
            })

        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            print(f"Error processing {file_key}: {error_code} - {error_msg}")

            results.append({
                'file': file_key,
                'status': 'error',
                'error': error_msg
            })

    return {
        'statusCode': 200,
        'body': json.dumps({
            'processed': len([r for r in results if r['status'] == 'success']),
            'errors': len([r for r in results if r['status'] == 'error']),
            'results': results
        })
    }
