# Day 1 Decisions

- Repository name: doc2order-inquiry-engine
- Multi-customer architecture: yes
- Core/orchestration stack: S3 + SQS + Lambda + Step Functions + DynamoDB
- Normalization boundary: mandatory
- Supported file types for MVP: PDF, XLSX
- Output formats for MVP: CSV, XLSX
- Primary customer for MVP: evapo
- Future-customer support: configuration-driven
- Draft order creation: out of scope