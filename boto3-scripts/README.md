# Boto3 AWS Automation Scripts

Three Python scripts demonstrating AWS automation with boto3.

## Scripts

### list_resources.py
Generates an inventory of AWS resources:
- All S3 buckets with creation dates
- All EC2 instances with state and type
- All IAM users

[Run python3](list_resources.py)

### upload_to_s3.py
Uploads files from local machine to S3:
- Accepts file path and bucket name
- Organises by date prefix (scripts/YYYY-MM-DD/)
- Lists bucket contents after upload

[Run python3](upload_to_s3.py)

### stop_instances.py
Safety-aware EC2 instance stopper:
- Finds all running instances
- Displays instance details with WARNING
- Requires typed confirmation before stopping
- Stops all running instances on confirmation

[Run python3](stop_instances.py)

## Security
- No credentials hardcoded in any script
- Uses ~/.aws/credentials via aws configure
- On EC2/Lambda: automatically uses IAM Role
