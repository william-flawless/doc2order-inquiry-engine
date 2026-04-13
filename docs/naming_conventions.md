# Naming Conventions

Pattern:
doc2order-inquiry-engine-{component}-{env}

Examples:
- doc2order-inquiry-engine-ingest-dev
- doc2order-inquiry-engine-pdf-parser-dev
- doc2order-inquiry-engine-reporting-dev
- doc2order-inquiry-engine-workflow-dev


# Environment and Customer Naming Conventions

## Environment Names

### Allowed values
- dev
- staging
- prod

### Definitions

#### dev
- purpose: active development and local/integration testing
- characteristics:
  - unstable
  - frequent deployments
  - test data only
- example usage:
  - S3: input/dev/evapo/
  - Lambda: doc2order-inquiry-engine-ingest-dev

#### staging
- purpose: pre-production validation and QA testing
- characteristics:
  - mirrors production behavior
  - used for end-to-end testing
  - may use near-real data (sanitized if required)
- example usage:
  - S3: input/staging/evapo/
  - Lambda: doc2order-inquiry-engine-ingest-staging

#### prod
- purpose: live production environment
- characteristics:
  - stable and controlled deployments
  - real customer data
  - strict monitoring and logging
- example usage:
  - S3: input/prod/evapo/
  - Lambda: doc2order-inquiry-engine-ingest-prod

### Rules
- environment names must always be lowercase
- environment must be explicitly passed in all processing contexts
- environment must be included in:
  - S3 paths
  - Lambda names
  - Step Functions
  - DynamoDB records
  - logs and audit outputs

---

## Customer ID Naming

### Format rules
- lowercase only
- alphanumeric + hyphens allowed
- no spaces
- no underscores
- must be URL-safe (slug format)

### Examples

Valid:
- evapo
- ace-of-vapes
- uk-flawless
- vape-club-london

Invalid:
- Evapo            (uppercase not allowed)
- ace_of_vapes     (underscore not allowed)
- Ace Of Vapes     (spaces not allowed)

### Definition

A customer_id is:
- a unique identifier for a client/customer
- used to isolate:
  - parsing rules
  - matching configurations
  - reporting formats
  - S3 storage paths

### Usage Examples

#### S3 paths
input/dev/evapo/
output/prod/ace-of-vapes/

#### Code structure
src/customers/evapo/
src/customers/ace-of-vapes/

#### Processing context
{
  "customer_id": "evapo"
}

---

## Combined Naming Patterns

### Resource naming

Pattern:
doc2order-inquiry-engine-{component}-{env}

Examples:
- doc2order-inquiry-engine-ingest-dev
- doc2order-inquiry-engine-pdf-parser-prod

---

### S3 path naming

Pattern:
{layer}/{env}/{customer_id}/

Examples:
- input/dev/evapo/
- output/prod/ace-of-vapes/

---

### Document-level paths

Pattern:
{layer}/{env}/{customer_id}/{yyyy}/{mm}/{dd}/{doc_id}/

Example:
output/prod/evapo/2026/04/13/abc123/report.csv

---

## Important Rules (Do Not Violate)

- Always include both environment and customer_id in all storage paths
- Never hardcode customer-specific logic outside `src/customers/`
- Never mix environments within the same processing flow
- Never use display names (e.g., "Evapo Ltd") as customer_id
- customer_id must remain stable over time (do not rename once used)

---

## Future Scalability Considerations

- New customers should only require:
  - a new folder under `src/customers/{customer_id}`
  - a config file (no core code changes)

- All pipelines must remain:
  - environment-aware
  - customer-aware
  - configuration-driven