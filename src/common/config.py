import os


APP_ENV = os.getenv("APP_ENV", "dev")
CUSTOMER_ID = os.getenv("CUSTOMER_ID", "evapo")

INPUT_BUCKET = os.getenv("INPUT_BUCKET", "")
OUTPUT_BUCKET = os.getenv("OUTPUT_BUCKET", "")
AUDIT_BUCKET = os.getenv("AUDIT_BUCKET", "")
VARIANTMASTER_BUCKET = os.getenv("VARIANTMASTER_BUCKET", "")
VARIANT_MASTER_KEY = os.getenv("VARIANT_MASTER_KEY", "")

PROCESSED_DOCS_TABLE = os.getenv("PROCESSED_DOCS_TABLE", "")

CANDIDATE_TOP_K = int(os.getenv("CANDIDATE_TOP_K", "5"))

ENABLE_OCR_FALLBACK = os.getenv("ENABLE_OCR_FALLBACK", "true").lower() == "true"
ENABLE_LLM_EXTRACTION = os.getenv("ENABLE_LLM_EXTRACTION", "true").lower() == "true"