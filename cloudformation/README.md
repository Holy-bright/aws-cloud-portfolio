# CloudFormation Templates

Infrastructure as Code templates for AWS resource deployment.

##[my_stack.yaml](my_stack.yaml)

Deploys a complete web application infrastructure:

| Resource | Type | Purpose |
|----------|------|---------|
| MyEC2Instance | AWS::EC2::Instance | Web server with Apache |
| MySecurityGroup | AWS::EC2::SecurityGroup | Firewall rules |
| MyS3Bucket | AWS::S3::Bucket | Storage with versioning |

### Parameters
- `InstanceType`: EC2 size (default: t2.micro)
- `Environment`: Deployment tag (default: learning)

### Deploy
1. CloudFormation Console → Create Stack
2. Upload my_stack.yaml
3. Enter parameter values
4. Review and create

### What I learned
- CloudFormation is declarative — define WHAT not HOW
- Templates are reusable across environments via Parameters
- Stacks group resources for lifecycle management
- Change sets allow safe preview before applying changes
- Drift detection catches manual changes to managed resources
- Stack deletion removes ALL resources automatically
