# Doc2Order Inquiry Engine

## Overview
A multi-customer engine for processing document-based stock inquiries and generating inventory availability reports.

## Inputs
- PDF
- XLSX

## Outputs
- CSV
- XLSX

## Core capabilities
- file ingestion
- parsing
- normalization
- candidate generation
- hybrid matching
- inventory lookup
- reporting
- audit logging

## Architecture
- AWS Lambda
- Amazon S3
- Amazon SQS
- AWS Step Functions
- DynamoDB

## Repository structure
- src/core: reusable engine components
- src/customers: customer-specific config
- src/common: shared config/schemas/utilities
- docs: design and decision docs

## Environments
- dev
- staging
- prod