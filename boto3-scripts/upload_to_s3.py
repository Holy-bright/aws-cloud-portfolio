import boto3
import os
from botocore.exceptions import ClientError
from datetime import datetime

def upload_file_to_s3(local_path, bucket_name, s3_key=None):
    if not os.path.exists(local_path):
        print(f"Error: File not found: {local_path}")
        return False

    if s3_key is None:
        s3_key = os.path.basename(local_path)

    file_size = os.path.getsize(local_path)
    print(f"Uploading: {local_path}")
    print(f"  → Bucket: {bucket_name}")
    print(f"  → Key:    {s3_key}")
    print(f"  → Size:   {file_size} bytes")

    try:
        s3 = boto3.client('s3')
        s3.upload_file(local_path, bucket_name, s3_key)
        print(f"  ✅ Upload successful!")

        url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
        print(f"  → URL: {url}")
        return True

    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"  ❌ Upload failed: {error_code}")
        print(f"  → {e.response['Error']['Message']}")
        return False

def list_bucket_contents(bucket_name):
    try:
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' not in response:
            print(f"\nBucket {bucket_name} is empty")
            return

        objects = response['Contents']
        total_size = sum(obj['Size'] for obj in objects)

        print(f"\n=== Contents of {bucket_name} ===")
        print(f"Total objects: {len(objects)}")
        print(f"Total size: {total_size:,} bytes")
        print()

        for obj in objects:
            size = obj['Size']
            modified = obj['LastModified'].strftime('%Y-%m-%d %H:%M')
            print(f"  {obj['Key']}")
            print(f"    Size: {size:,} bytes | Modified: {modified}")

    except ClientError as e:
        print(f"Error listing bucket: {e.response['Error']['Message']}")

# ─── MAIN ─────────────────────────────────────────
print("=" * 50)
print("S3 FILE UPLOADER")
print("=" * 50)

YOUR_BUCKET = "bright-cloud-portfolio-bright"

files_to_upload = [
    "/home/kali/cloud_journey/projects/health_report.sh",
    "/home/kali/cloud_journey/projects/progress_tracker.py",
]

timestamp = datetime.now().strftime('%Y-%m-%d')
success_count = 0

for file_path in files_to_upload:
    filename = os.path.basename(file_path)
    s3_key = f"scripts/{timestamp}/{filename}"

    print()
    success = upload_file_to_s3(file_path, YOUR_BUCKET, s3_key)
    if success:
        success_count += 1

print()
print(f"Upload complete: {success_count}/{len(files_to_upload)} files uploaded")

list_bucket_contents(YOUR_BUCKET)
