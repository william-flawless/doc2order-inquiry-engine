# Normalized Schema

## Required fields
- row_id
- doc_id
- customer_id
- source_file_name
- source_file_type
- customer_product_description
- raw_row_data
- extraction_method
- parser_version

## Optional fields
- source_sheet_name
- source_page_number
- requested_quantity
- requested_uom
- normalization_warnings

### row_id
- type: string
- required: yes
- example: "row_0001"
- notes: unique identifier for each extracted row within a document; must be deterministic or sequential per document to ensure traceability

### doc_id
- type: string
- required: yes
- example: "evapo_abc123_hash"
- notes: unique identifier for the processed document; typically derived from bucket + key + etag + customer_id to enforce idempotency

### customer_id
- type: string
- required: yes
- example: "evapo"
- notes: normalized identifier for the customer; used to load customer-specific configuration, parsing rules, and matching behavior

### source_file_name
- type: string
- required: yes
- example: "stock_inquiry_apr13.pdf"
- notes: original file name extracted from the S3 object key or metadata; used for reporting and traceability

### source_file_type
- type: string (enum: "pdf", "xlsx")
- required: yes
- example: "pdf"
- notes: detected file type used to route parsing logic; must be validated during ingestion

### customer_product_description
- type: string
- required: yes
- example: "Elf Bar Blue Razz Lemonade"
- notes: raw or lightly cleaned product description extracted from the source document; primary input for matching logic

### raw_row_data
- type: json (object)
- required: yes
- example: {"column_1": "Elf Bar Blue Razz Lemonade", "column_2": "20"}
- notes: full raw representation of the extracted row (original columns, text, or OCR output); used for debugging, audit, and traceability

### extraction_method
- type: string (enum: "deterministic_pdf", "ocr_pdf", "llm_pdf", "xlsx_mapping")
- required: yes
- example: "xlsx_mapping"
- notes: indicates how the row was extracted; critical for auditability and performance monitoring of parsing strategies

### parser_version
- type: string
- required: yes
- example: "v1.0.0"
- notes: version identifier of the parsing logic used; allows tracking of changes and reproducibility of extraction behavior

### source_sheet_name
- type: string
- required: no
- example: "Sheet1"
- notes: name of the Excel sheet where the row was extracted; applicable only for XLSX inputs

### source_page_number
- type: integer
- required: no
- example: 1
- notes: page number within the PDF where the row was extracted; useful for traceability and debugging parsing issues

### requested_quantity
- type: number (float or integer)
- required: no
- example: 20
- notes: quantity requested by the customer; may be null if not present or not reliably extracted from the source

### requested_uom
- type: string
- required: no
- example: "pcs"
- notes: unit of measure associated with the requested quantity (e.g., pcs, boxes, cartons); may require normalization across customers

### normalization_warnings
- type: array[string]
- required: no
- example: ["missing_quantity", "ambiguous_header_mapping"]
- notes: list of warnings generated during normalization (e.g., missing fields, uncertain mappings); used for downstream QA and monitoring