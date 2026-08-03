# Serverless Image Processing Pipeline

A production-pattern serverless architecture using five
AWS services working together automatically.

## Architecture
[Pipeline Architecture](pipeline_architecture.png)

## Services Used

| Service | Role |
|---------|------|
| S3 (uploads) | Trigger source — receives uploaded files |
| S3 (processed) | Output destination — stores processed files |
| Lambda | Processing engine — orchestrates the pipeline |
| DynamoDB | Audit log — records every processed file |
| SNS | Notifications — emails on every successful process |
| CloudWatch | Monitoring — alerts on errors and slow executions |

## How It Works
1. File uploaded to bright-uploads S3 bucket
2. S3 Event Notification triggers Lambda automatically
3. Lambda reads file metadata from the S3 event
4. Lambda copies file to bright-processed bucket
5. Lambda writes audit log entry to DynamoDB
6. Lambda publishes success notification via SNS
7. CloudWatch monitors for errors and duration issues

## Lambda Code
[View Script](lambda_function.py)

## Key Design Decisions
- Clients initialised outside handler for warm start performance
- Error handling per record so one failure does not stop others
- Separate buckets for uploads and processed files
- DynamoDB sort key includes timestamp for chronological queries
- SNS used for both pipeline notifications and CloudWatch alerts

## Skills Demonstrated
- S3 Event Notifications triggering Lambda
- Multi-service boto3 integration in one function
- DynamoDB write operations from Lambda
- SNS publish from Lambda
- CloudWatch alarm configuration
- IAM role with least-privilege permissions
- Error handling with ClientError
- Warm start optimisation (clients outside handler)
