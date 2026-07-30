import boto3
from botocore.exceptions import ClientError

def get_instance_name(instance):
    tags = instance.get('Tags', [])
    for tag in tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return 'Unnamed'

def find_running_instances(region):
    ec2 = boto3.client('ec2', region_name=region)

    response = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    running = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            running.append({
                'id': instance['InstanceId'],
                'type': instance['InstanceType'],
                'name': get_instance_name(instance),
                'launch_time': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M')
            })

    return running

def stop_instances(region, instance_ids):
    ec2 = boto3.client('ec2', region_name=region)

    try:
        response = ec2.stop_instances(InstanceIds=instance_ids)
        stopping = response['StoppingInstances']

        for item in stopping:
            instance_id = item['InstanceId']
            prev_state = item['PreviousState']['Name']
            curr_state = item['CurrentState']['Name']
            print(f"  {instance_id}: {prev_state} → {curr_state}")

        return True

    except ClientError as e:
        print(f"Error stopping instances: {e.response['Error']['Message']}")
        return False

# ─── MAIN ─────────────────────────────────────────
REGION = 'us-east-1'

print("=" * 50)
print("EC2 INSTANCE STOP UTILITY")
print("=" * 50)
print(f"Region: {REGION}")
print()

print("Scanning for running instances...")
running_instances = find_running_instances(REGION)

if not running_instances:
    print("No running instances found.")
    print("Nothing to stop.")
    exit(0)

print(f"\n⚠️  WARNING: Found {len(running_instances)} running instance(s):\n")

for instance in running_instances:
    print(f"  Instance:  {instance['id']}")
    print(f"  Name:      {instance['name']}")
    print(f"  Type:      {instance['type']}")
    print(f"  Launched:  {instance['launch_time']}")
    print()

print("─" * 50)
print("⚠️  You are about to STOP these instances.")
print("   Data will be preserved but instances will stop.")
print("   Running costs will pause after stopping.")
print("─" * 50)
print()

confirmation = input("Type YES to stop all instances, or anything else to cancel: ")

if confirmation.strip().upper() == "YES":
    print()
    print("Stopping instances...")

    instance_ids = [i['id'] for i in running_instances]
    success = stop_instances(REGION, instance_ids)

    if success:
        print()
        print(f"✅ Successfully initiated stop for {len(instance_ids)} instance(s)")
        print("   Instances will reach 'stopped' state in 30-60 seconds")
        print("   Check AWS Console to confirm")
    else:
        print("❌ Stop operation failed. Check errors above.")
else:
    print()
    print("Cancelled. No instances were stopped.")
    print("All instances remain running.")
