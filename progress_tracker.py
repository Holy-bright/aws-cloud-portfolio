import json
import datetime

# Step 1: Create your study progress dictionary
progress = {
    'Linux': 'complete',
    'Networking': 'complete',
    'EC2': 'complete',
    'S3': 'complete',
    'VPC': 'complete',
    'IAM': 'complete',
    'Lambda': 'complete',
    'Docker': 'complete',
    'DynamoDB': 'complete',
    'CloudTrail': 'complete',
    'Python': 'in progress'
}

# Step 2: Function to format each topic's status
def format_status(topic, status):
    if status == 'complete':
        return f"{topic}: ✅ COMPLETE"
    elif status == 'in progress':
        return f"{topic}: 🔄 IN PROGRESS"
    else:
        return f"{topic}: ⏳ NOT STARTED"

# Step 3: Loop through and print each topic
print("=" * 40)
print("CLOUD ENGINEERING STUDY PROGRESS")
print("=" * 40)

completed_count = 0
total_count = len(progress)
report_lines = []

for topic, status in progress.items():
    formatted = format_status(topic, status)
    print(formatted)
    report_lines.append(formatted)

    if status == 'complete':
        completed_count += 1

# Step 4: Print summary
print("=" * 40)
summary = f"You have completed {completed_count} out of {total_count} topics"
print(summary)

percentage = (completed_count / total_count) * 100
progress_bar = f"Progress: {percentage:.1f}%"
print(progress_bar)
print("=" * 40)

# Step 5: Write report to file
today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
report_filename = "study_progress.txt"

with open(report_filename, "w") as file:
    file.write("CLOUD ENGINEERING STUDY PROGRESS REPORT\n")
    file.write(f"Generated: {today}\n")
    file.write("=" * 40 + "\n")

    for line in report_lines:
        file.write(line + "\n")

    file.write("=" * 40 + "\n")
    file.write(summary + "\n")
    file.write(progress_bar + "\n")

print(f"\nReport saved to: {report_filename}")
