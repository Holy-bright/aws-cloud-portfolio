## Scenario 1: EC2 running but cannot SSH

**Step 1 — Identify the problem:**
Exact symptom: SSH times out or connection refused.
Questions I ask:
  - What error exactly: "Connection timed out" or "Connection refused"?
  - Timeout = blocked before reaching EC2 (firewall/network)
  - Refused = reached EC2 but SSH daemon rejected it
  - What OS is the instance running? (determines correct username)
  - Has the instance been restarted recently? (public IP changes)
  - What changed since it last worked?

**Step 2 — Establish a theory (in order of likelihood):**
  1. Security Group not allowing SSH from current IP (most common)
  2. No public IP assigned or IP changed after restart
  3. Wrong username for the OS
  4. Key pair mismatch or wrong permissions on .pem file
  5. NACL blocking traffic at subnet level
  6. Route table missing Internet Gateway route
  7. SSH daemon not running inside instance

**Step 3 — Test the theory (specific steps):**

Check 1: Public IP
  EC2 → Instances → select instance
  Look for: Public IPv4 address
  If None: instance has no public IP → this is the cause

Check 2: Security Group
  EC2 → Instances → Security tab → Security groups
  Click the security group → Inbound rules
  Look for: Type=SSH, Port=22, Source=My IP or 0.0.0.0/0
  If missing: security group is blocking SSH → this is the cause
  Run from terminal to confirm blocking:
    nc -zv YOUR_EC2_IP 22
    Connection timeout = blocked
    Connection refused = reached instance, SSH daemon issue

Check 3: Key pair and permissions
  ls -la ~/.ssh/bright-key.pem
  Should show: -r-------- (400)
  If not: chmod 400 ~/.ssh/bright-key.pem
  Correct username per OS:
    Amazon Linux: ec2-user
    Ubuntu:       ubuntu
    RHEL:         ec2-user
    Debian:       admin

Check 4: NACL
  VPC → Network ACLs → find NACL for instance subnet
  Inbound: must allow TCP port 22 from your IP
  Outbound: must allow TCP ports 1024-65535 (ephemeral)
  (NACLs are stateless — both directions needed)

Check 5: Route Table
  VPC → Route Tables → find table for instance subnet
  Must have: 0.0.0.0/0 → igw-xxxxxxxx
  If missing: no internet access from this subnet

Check 6: Instance Status Checks
  EC2 → Instances → Status checks tab
  Should show: 2/2 checks passed
  If failed: instance OS may be unresponsive
  Use: EC2 Instance Connect (browser-based SSH)
  Or: EC2 Serial Console for deeper debugging

**Step 4 — Action plan:**
Based on finding in Step 3, fix the specific layer:
  SG issue:    Add inbound rule TCP 22 from My IP
  No IP:       Actions → Networking → Manage IP addresses
               or allocate Elastic IP
  Key issue:   chmod 400 ~/.ssh/bright-key.pem
  NACL issue:  Add inbound rule 100 ALLOW TCP 22
               Add outbound rule 100 ALLOW TCP 1024-65535
  Route issue: Add route 0.0.0.0/0 → Internet Gateway

**Step 5 — Verify and document:**
  ssh -i ~/.ssh/bright-key.pem ec2-user@YOUR_EC2_IP
  Expected: successful login, see bash prompt
  Monitor for 10 minutes to confirm stable
  
  Document:
    Root cause: [specific finding]
    Fix applied: [specific change made]
    Time to resolve: X minutes
    Prevention: [what would prevent recurrence]

## Scenario 2: 502 Bad Gateway through ALB

**Step 1 — Identify the problem:**
502 specifically means: ALB reached the target but received
an invalid response. Different from:
  503 = no healthy targets available
  504 = target did not respond in time

Questions I ask:
  - Is it all users or some users?
  - Is it all requests or specific paths?
  - When did it start? What changed?
  - Is the EC2 instance running?

**Step 2 — Establish a theory (in order of likelihood):**
  1. Application crashed or not running on EC2 (most common)
  2. Application running on wrong port
  3. Health check path returning non-200 status
  4. Security group between ALB and EC2 blocking traffic
  5. Target group pointing to wrong port
  6. Application throwing 500 errors that ALB surfaces as 502

**Step 3 — Test the theory:**

Check 1: Target Group health
  EC2 → Target Groups → select your target group
  Targets tab → health status column
  Healthy: green circle
  Unhealthy: red circle → click target → see health check details
  Note the failure reason shown

Check 2: Is application running on EC2
  SSH into the EC2 instance
  sudo systemctl status httpd    (Amazon Linux Apache)
  sudo systemctl status nginx    (nginx)
  sudo systemctl status your-app
  If not running: this is the cause

Check 3: Is application listening on correct port
  On EC2 via SSH:
  ss -tlnp | grep :80
  Should show: LISTEN on 0.0.0.0:80
  If different port: target group pointing to wrong port

Check 4: Test application directly
  On EC2 via SSH:
  curl -I http://localhost:80
  Should return: HTTP/1.1 200 OK
  If not 200: application error, check application logs

Check 5: Security group between ALB and EC2
  EC2 security group inbound rules
  Must allow traffic from ALB security group (not 0.0.0.0/0)
  Source should be the ALB security group ID

Check 6: ALB Access Logs (if enabled)
  S3 → ALB access log bucket
  grep for 502 responses
  Shows exact backend response that caused 502

**Step 4 — Action plan:**
  App crashed: sudo systemctl start httpd && systemctl enable httpd
  Wrong port:  Update target group port to match application
  SG issue:    Add inbound rule from ALB security group
  App errors:  Fix application code, check /var/log/httpd/error_log

**Step 5 — Verify and document:**
  curl -I http://YOUR_ALB_DNS_NAME
  Expected: HTTP/1.1 200 OK
  CloudWatch → ALB → HTTPCode_ELB_5XX → confirm dropping to 0
  Monitor target group health for 5 minutes → all healthy
  
  Document root cause, fix, and add health check monitoring alert

## Scenario 3: Lambda Access Denied on S3

**Step 1 — Identify the problem:**
Lambda function returning AccessDenied on S3 operation.
Questions I ask:
  - What exact S3 operation is failing? GetObject? PutObject? ListBucket?
  - What changed between yesterday and today?
    (someone may have changed IAM role, bucket policy, or encryption)
  - Is it all S3 buckets or one specific bucket?
  - When exactly did it start failing?

**Step 2 — Establish a theory (in order of likelihood):**
  1. IAM execution role missing required S3 permission
  2. Bucket policy added explicit Deny for Lambda role
  3. Bucket encryption changed to SSE-KMS, role lacks kms:Decrypt
  4. Block Public Access settings changed on bucket
  5. Explicit Deny added somewhere overriding the Allow
  6. Lambda role was modified or replaced

**Step 3 — Test the theory:**

Check 1: CloudTrail — find the exact denied call
  CloudTrail → Event History
  Filter: Event name = GetObject (or whatever is failing)
  Filter: Time = last 24 hours
  Find the FAILED event → click it
  Shows: exact error, exact resource ARN, exact principal
  Note the exact error code: AccessDenied

Check 2: Lambda execution role
  Lambda → your function → Configuration → Permissions
  Click the execution role name → opens IAM
  Check attached policies
  Look for: s3:GetObject (or the failing action) on the bucket
  If missing: this is the cause

Check 3: IAM Policy Simulator
  IAM → Policy Simulator
  Select the Lambda execution role
  Service: S3, Action: GetObject, Resource: the bucket ARN
  Shows: Allowed or Denied and which policy is causing it

Check 4: S3 Bucket Policy
  S3 → your bucket → Permissions → Bucket Policy
  Look for explicit Deny statements
  Look for conditions that might exclude the Lambda role
  Check if Lambda role ARN is in any Deny Principal

Check 5: KMS encryption
  S3 → your bucket → Properties → Default Encryption
  If SSE-KMS: Lambda role needs kms:Decrypt AND kms:GenerateDataKey
  IAM → Lambda role → check for KMS permissions
  KMS → the key → Key policy → check Lambda role is allowed

Check 6: What changed yesterday
  CloudTrail → filter by yesterday's date
  Look for: PutBucketPolicy, PutRolePolicy, PutKeyPolicy
  Shows exactly what was changed and who changed it

**Step 4 — Action plan:**
  Missing IAM permission: add s3:GetObject to Lambda role policy
  Bucket policy Deny: remove or update the Deny statement
  KMS issue: add kms:Decrypt and kms:GenerateDataKey to role
  
  Use minimal permissions — add only what is needed

**Step 5 — Verify and document:**
  Lambda → Test → run with event that triggers S3 access
  CloudWatch Logs → confirm no AccessDenied errors
  Document: what changed, what permission was missing, who changed it
  Add Config rule: lambda-function-public-access-prohibited

## Scenario 4: S3 Objects Return 403 Forbidden

**Step 1 — Identify the problem:**
403 Forbidden on S3 objects from website.
Questions I ask:
  - Is it one object or all objects?
  - Did it ever work or is this a new setup?
  - What is the exact URL being used?
  - Has anything changed recently on the bucket?

**Step 2 — Establish a theory (in order of likelihood):**
  1. Block Public Access enabled at bucket or account level
  2. Bucket policy missing or not granting public read
  3. Object URL format incorrect (wrong region in URL)
  4. Object does not exist at that key path
  5. Requester Pays enabled on bucket
  6. Object encrypted with SSE-KMS (cannot be public)

**Step 3 — Test the theory:**

Check 1: Account-level Block Public Access
  S3 → Block Public Access settings for this account (top level)
  If any of the four settings are ON at account level:
  They override ALL bucket policies → nothing can be public
  This is the most common cause people miss

Check 2: Bucket-level Block Public Access
  S3 → your bucket → Permissions → Block public access (bucket settings)
  All four should be OFF for a public website bucket

Check 3: Bucket Policy
  S3 → your bucket → Permissions → Bucket Policy
  Should contain:
    Effect: Allow
    Principal: "*"
    Action: "s3:GetObject"
    Resource: "arn:aws:s3:::bucket-name/*"
  If missing: add it
  If Principal is not "*": objects not publicly readable

Check 4: Test the URL directly
  Open browser and paste:
  https://BUCKET-NAME.s3.REGION.amazonaws.com/OBJECT-KEY
  404 = object does not exist at that path
  403 = exists but access denied (policy issue)
  200 = working correctly

Check 5: Verify object exists with correct key
  S3 → bucket → Objects tab
  Find the exact object
  Compare the key shown with the URL being used
  Keys are case sensitive: image.jpg ≠ Image.jpg

Check 6: Object encryption
  Click the object → Properties → Server-side encryption
  If SSE-KMS: cannot be served publicly regardless of policy

**Step 4 — Action plan:**
  Account BPA: only disable if truly intentional
  Bucket BPA: disable all four settings
  Bucket policy: add correct Allow statement
  Wrong URL: fix the URL path to match exact object key

**Step 5 — Verify and document:**
  curl -I "https://BUCKET.s3.REGION.amazonaws.com/OBJECT-KEY"
  Expected: HTTP/1.1 200 OK
  Open the webpage and confirm image loads
  Document: which setting was blocking access and why

## Scenario 5: RDS Timing Out from EC2

**Step 1 — Identify the problem:**
EC2 application cannot connect to RDS, times out.
Questions I ask:
  - Timeout or connection refused? (different causes)
  - Was it working before or is this new?
  - Has anything changed in the VPC or security groups?
  - What database engine and port? (MySQL=3306, Postgres=5432)
  - Are credentials correct? (separate from network issue)

**Step 2 — Establish a theory (in order of likelihood):**
  1. RDS Security Group not allowing EC2 Security Group on port 3306
  2. EC2 and RDS in different VPCs with no peering
  3. NACL blocking traffic between subnets
  4. RDS instance stopped or in maintenance
  5. Wrong endpoint URL (using IP instead of DNS endpoint)
  6. Max connections reached on RDS
  7. Incorrect credentials (separate issue — connection refused not timeout)

**Step 3 — Test the theory:**

Check 1: RDS instance status
  RDS → Databases → select your database
  Status must be: Available
  Not: Stopped, Modifying, Backing-up, Failed

Check 2: Network connectivity test from EC2
  SSH into EC2 instance
  nc -zv YOUR-RDS-ENDPOINT.rds.amazonaws.com 3306
  Timeout = network blocked (SG, NACL, or VPC issue)
  Connection refused = reached RDS but rejected
  Success = network works, problem is credentials or app config

Check 3: RDS Security Group inbound rules
  RDS → your database → Connectivity & security
  Click the VPC security group
  Inbound rules:
    Type: MySQL/Aurora
    Port: 3306
    Source: EC2 security group ID (sg-xxxxxxxx)
  If source is 0.0.0.0/0 or wrong SG: fix this

Check 4: Are EC2 and RDS in same VPC
  EC2 → instance → VPC ID: note it
  RDS → database → VPC: note it
  Must be the same VPC
  If different: VPC peering needed or wrong configuration

Check 5: NACL between subnets
  VPC → Network ACLs
  Find NACL for EC2 subnet: allows outbound to port 3306?
  Find NACL for RDS subnet: allows inbound on port 3306?
  Find NACL for RDS subnet: allows outbound ephemeral ports?
  NACLs are stateless — both directions needed

Check 6: RDS endpoint
  RDS → database → Connectivity → Endpoint
  Application must use the DNS endpoint not an IP address
  RDS IPs change — DNS endpoint is stable

Check 7: Connection limits
  CloudWatch → RDS → DatabaseConnections metric
  Near max_connections? New connections rejected
  Fix: increase instance size or implement RDS Proxy

**Step 4 — Action plan:**
  SG issue: add inbound rule port 3306 from EC2 security group
  Different VPC: set up VPC peering or move to same VPC
  NACL issue: add correct inbound and outbound rules
  Endpoint: update application config to use DNS endpoint
  Connections: add RDS Proxy or increase instance size

**Step 5 — Verify and document:**
  nc -zv YOUR-RDS-ENDPOINT 3306
  Expected: Connection to endpoint port 3306 succeeded!
  Test from application: run a simple database query
  Monitor CloudWatch DatabaseConnections for stability
  
  Document: exact layer that was blocking, change made,
  add CloudWatch alarm on DatabaseConnections going forward

