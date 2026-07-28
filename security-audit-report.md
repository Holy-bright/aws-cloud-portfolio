# AWS Security Audit Report

**Account:** Redacted for security
**Date:** July 2026
**Auditor:** HolyBright
**Purpose:** Monthly security assessment of an AWS account

---

## Executive Summary

This report documents the results of a security audit performed on my AWS learning account. The audit evaluated nine key security controls covering identity management, storage security, logging, monitoring, and network security.

**Results:** **9 PASS / 0 FAIL**

The environment follows AWS security best practices including Multi-Factor Authentication (MFA), least privilege access, encrypted storage, centralized logging, threat detection, and restricted network access.

---

# Audit Findings

## 1. MFA on Root Account

**Status:** ✅ PASS

**Check:**
Root account has Multi-Factor Authentication enabled.

**Finding:**
Virtual MFA is enabled, providing an additional authentication factor for privileged account access.

**Risk if FAIL:**
A compromised root password could result in complete AWS account takeover.

**Remediation:**
Enable MFA using a supported authenticator application.

---

## 2. No Root Access Keys

**Status:** ✅ PASS

**Check:**
Root account has no active access keys.

**Finding:**
No root access keys exist. Administrative access is performed using IAM identities following AWS best practices.

**Risk if FAIL:**
Leaked root access keys provide unrestricted account access.

**Remediation:**
Delete all root access keys immediately.

---

## 3. IAM Password Policy

**Status:** ✅ PASS

**Check:**

- Minimum 12 characters
- Uppercase letters
- Lowercase letters
- Numbers
- Special characters
- Password expiration enabled
- Password reuse prevention enabled

**Finding:**
The account password policy meets recommended AWS security standards.

**Risk if FAIL:**
Weak passwords increase the likelihood of brute-force and credential stuffing attacks.

**Remediation:**
Review IAM Account Settings and enforce a strong password policy.

---

## 4. S3 Bucket Encryption

**Status:** ✅ PASS

**Check:**
Default encryption enabled on all S3 buckets.

**Buckets Reviewed:**

- Portfolio bucket — Encrypted
- Static website assets bucket — Encrypted

**Finding:**
All buckets use server-side encryption (SSE) by default.

**Risk if FAIL:**
Unencrypted objects could be exposed if unauthorized access occurs.

**Remediation:**
Enable SSE-S3 or SSE-KMS for all buckets.

---

## 5. S3 Public Access

**Status:** ✅ PASS

**Check:**
Review public accessibility of all S3 buckets.

**Finding:**

- Static website assets bucket intentionally allows public read access for website content.
- All remaining buckets have Block Public Access enabled.

This public bucket is a documented exception required for static website hosting.

**Risk if FAIL:**
Sensitive data could become publicly accessible.

**Remediation:**
Keep Block Public Access enabled except where business requirements explicitly require public content.

---

## 6. CloudTrail Multi-Region Logging

**Status:** ✅ PASS

**Check:**
CloudTrail enabled across all AWS Regions.

**Finding:**

- Multi-Region trail configured
- Logs delivered securely to Amazon S3
- Log file validation enabled
- Encryption enabled

**Risk if FAIL:**
API activity in unmonitored Regions would not be recorded.

**Remediation:**
Deploy a Multi-Region CloudTrail with secure S3 log storage.

---

## 7. GuardDuty Enabled

**Status:** ✅ PASS

**Check:**
Amazon GuardDuty enabled.

**Finding:**

- Threat detection active
- No High severity findings detected during the audit
- Continuous monitoring enabled

**Risk if FAIL:**
Compromised credentials and suspicious activity may go undetected.

**Remediation:**
Enable GuardDuty and review findings regularly.

---

## 8. Billing Alarm

**Status:** ✅ PASS

**Check:**
CloudWatch billing alarm configured.

**Finding:**
Billing alert configured to notify when estimated monthly charges exceed the defined budget threshold.

**Risk if FAIL:**
Unexpected costs may remain unnoticed until the billing cycle ends.

**Remediation:**
Configure CloudWatch billing alarms with Amazon SNS notifications.

---

## 9. SSH Not Open to the Internet

**Status:** ✅ PASS

**Check:**
Review all Security Groups for unrestricted SSH access.

**Security Groups Reviewed:**

- Web Server Security Group — SSH restricted to administrator IP
- Database Security Group — Database access restricted to application Security Group
- Application Security Group — Least privilege rules applied

**Finding:**
No Security Group allows SSH access from `0.0.0.0/0`.

Administrative SSH access is restricted to a trusted public IP address only.

**Risk if FAIL:**
Internet-facing SSH endpoints are frequently targeted by automated attacks.

**Remediation:**
Restrict SSH access to trusted IP ranges or use AWS Systems Manager Session Manager.

---

# Recommendations

## Immediate Actions

No critical findings were identified during this assessment.

---

## Short-Term Improvements

- Enable AWS Config compliance rules
- Schedule monthly IAM access reviews
- Enable S3 Server Access Logging where appropriate
- Review GuardDuty findings weekly
- Rotate credentials regularly

---

## Long-Term Improvements

- Implement AWS Security Hub
- Deploy AWS Organizations for centralized governance
- Evaluate AWS Control Tower for multi-account management
- Create documented incident response runbooks
- Automate compliance reporting

---

# Tools Used

- AWS Identity and Access Management (IAM)
- Amazon S3
- AWS CloudTrail
- Amazon GuardDuty
- Amazon CloudWatch
- AWS Config
- Amazon EC2 Security Groups
- AWS Management Console

---

# Conclusion

The security assessment reviewed nine critical AWS security controls.

**Overall Result**

- ✅ Controls Passed: **9**
- ❌ Controls Failed: **0**

The environment follows AWS security best practices by implementing strong identity protection, encrypted storage, centralized audit logging, continuous threat detection, billing monitoring, and tightly controlled network access.

This assessment demonstrates a defense-in-depth approach suitable for a cloud learning environment while reinforcing AWS Well-Architected Security Pillar principles.

---

*This security audit was conducted as part of a hands-on AWS Cloud Engineering portfolio project focused on implementing and validating AWS security best practices.*
