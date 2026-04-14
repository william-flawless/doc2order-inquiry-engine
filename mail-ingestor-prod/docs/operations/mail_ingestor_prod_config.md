# Mail Ingestor (Prod) Configuration

## Overview
This document defines the production configuration for the `doc2order-inquiry-engine-mail-ingestor-prod` Lambda.

This Lambda:
- reads unread emails via Microsoft Graph
- filters for stock inquiry emails
- extracts supported attachments
- routes valid files to S3
- stores processing state
- moves processed emails to a designated folder

---

## Core Resource Names

### Lambda
- name: doc2order-inquiry-engine-mail-ingestor-prod

### IAM Role
- name: doc2order-inquiry-engine-mail-ingestor-prod-role

### S3 Bucket
- name: flawless-doc2order-inquiry-engine-prod

---

## S3 Paths

### Input Prefix
- path: input/prod/evapo/
- description: accepted inquiry files routed for downstream processing

### Quarantine Prefix
- path: quarantine/prod/
- description: rejected files (non-inquiry, unsupported, or no customer detected)

### State Key
- path: state/mail-ingestor/prod/state.json
- description: tracks processed message IDs to prevent reprocessing

---

## Email Processing Configuration

### Processed Folder Name (Microsoft Graph)
- value: Processed/Doc2OrderInquiryEngine
- description: destination folder where processed emails are moved

### Graph Secret ARN
- value: <REPLACE_WITH_ACTUAL_ARN>
- description: AWS Secrets Manager ARN containing Microsoft Graph credentials

---

## Scheduling

### EventBridge Rule
- name: doc2order-inquiry-engine-mail-ingestor-prod-schedule

### Schedule Interval
- value: rate(5 minutes)

---

## Processing Limits

### Max Messages Per Run
- value: 25

### Max File Size
- value: 15 MB

### Max Extracted Text Bytes
- value: 500,000 bytes

---

## Inquiry Detection

### Keyword List (Current)
```json
["stock inquiry", "stock enquiry"]