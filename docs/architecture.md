# Doc2Order Inquiry Engine - Architecture

## Purpose
Process customer stock inquiry documents and generate inventory availability reports.

## Supported input formats
- PDF
- XLSX

## Core stages
1. Ingest
2. Classify
3. Parse
4. Normalize
5. Candidate generation
6. Match
7. Inventory lookup
8. Report generation
9. Audit logging

## AWS services
- S3
- SQS
- Lambda
- Step Functions
- DynamoDB
- Secrets Manager
- Parameter Store

## Design principles
- Multi-customer
- Environment-aware
- Deterministic before LLM
- Strict normalization boundary
- Fully auditable
- Idempotent

## Out of scope
- Draft order creation
- Core logic in VBA
- Hardcoded customer schemas