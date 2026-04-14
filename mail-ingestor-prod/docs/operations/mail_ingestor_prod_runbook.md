# Mail Ingestor (Prod) Runbook

## Purpose
Operational guide for managing the `doc2order-inquiry-engine-mail-ingestor-prod` Lambda.

---

## Normal Operation

- Lambda runs every 5 minutes via EventBridge
- Reads unread emails
- Processes supported attachments
- Moves emails to processed folder
- Writes files to S3

---

## Manual Invocation

```bash
aws lambda invoke \
  --function-name doc2order-inquiry-engine-mail-ingestor-prod \
  --payload '{}' \
  response.json