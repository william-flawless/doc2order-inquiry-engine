# Mail Ingestor (Prod) Troubleshooting

---

## Issue: No files appearing in S3

### Possible Causes
- no unread emails
- inquiry keywords not matched
- attachments not supported
- Graph API failure

### Actions
- check CloudWatch logs
- temporarily log inquiry detection output
- test with known inquiry email

---

## Issue: Emails not being moved

### Possible Causes
- incorrect folder name
- Graph permissions issue

### Actions
- verify PROCESSED_FOLDER_NAME
- check Graph API logs
- manually test move endpoint

---

## Issue: Duplicate processing

### Possible Causes
- state file not updated
- concurrency > 1

### Actions
- verify state file path
- confirm reserved concurrency = 1

---

## Issue: Too many irrelevant emails processed

### Cause
- keyword list too broad

### Fix
- restrict to:
  ["stock inquiry", "stock enquiry"]

---

## Issue: Lambda timeout

### Cause
- too many large attachments

### Fix
- increase timeout
- reduce MAX_MESSAGES_PER_RUN

---

## Issue: Permission errors

### Check
- IAM role has:
  - s3:PutObject
  - secretsmanager:GetSecretValue
  - CloudWatch logging

---

## Debug Strategy

1. invoke manually
2. inspect logs
3. inspect S3
4. inspect state file
5. inspect mailbox