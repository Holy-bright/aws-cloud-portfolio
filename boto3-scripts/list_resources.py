import boto3
from botocore.exceptions import ClientError
from datetime import datetime

print("=" * 50)
print("AWS RESOURCE INVENTORY")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 50)

# ─── S3 BUCKETS ───────────────────────────────────
try:
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    buckets = response['Buckets']

    print(f"\n=== S3 BUCKETS ({len(buckets)} found) ===")

    if buckets:
        for bucket in buckets:
            name = bucket['Name']
            created = bucket['CreationDate'].strftime('%Y-%m-%d')
            print(f"  - {name} (created: {created})")
    else:
        print("  No S3 buckets found")

except ClientError as e:
    print(f"  Error listing S3 buckets: {e.response['Error']['Message']}")

# ─── EC2 INSTANCES ────────────────────────────────
try:
    ec2 = boto3.client('ec2', region_name='af-south-1')
    response = ec2.describe_instances()
    reservations = response['Reservations']

    instance_count = sum(len(r['Instances']) for r in reservations)
    print(f"\n=== EC2 INSTANCES ({instance_count} found) ===")

    if reservations:
        for reservation in reservations:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                state = instance['State']['Name']

                tags = instance.get('Tags', [])
                name = next(
                    (t['Value'] for t in tags if t['Key'] == 'Name'),
                    'Unnamed'
                )

                state_icon = "🟢" if state == "running" else "🔴"
                print(f"  {state_icon} {name} ({instance_id})")
                print(f"     Type: {instance_type} | State: {state}")
    else:
        print("  No EC2 instances found")

except ClientError as e:
    print(f"  Error listing EC2 instances: {e.response['Error']['Message']}")

# ─── IAM USERS ────────────────────────────────────
try:
    iam = boto3.client('iam')
    response = iam.list_users()
    users = response['Users']

    print(f"\n=== IAM USERS ({len(users)} found) ===")

    for user in users:
        username = user['UserName']
        created = user['CreateDate'].strftime('%Y-%m-%d')
        print(f"  - {username} (created: {created})")

except ClientError as e:
    print(f"  Error listing IAM users: {e.response['Error']['Message']}")

print("\n" + "=" * 50)
print("Inventory complete")
print("=" * 50)
