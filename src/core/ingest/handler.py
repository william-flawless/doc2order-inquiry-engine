import json
import os
from pathlib import Path

from src.common.hash_utils import make_doc_id
from src.common.idempotency import make_ttl, try_register_document
from src.common.logging_utils import get_logger
from src.common.s3_event_parser import parse_sqs_wrapped_s3_event

logger = get_logger(__name__)

APP_ENV = os.getenv("APP_ENV", "dev")
DEFAULT_CUSTOMER_ID = os.getenv("CUSTOMER_ID", "evapo")


def detect_file_type(key: str) -> str:
    suffix = Path(key).suffix.lower()
    if suffix == ".pdf":
        return "pdf"
    if suffix == ".xlsx":
        return "xlsx"
    return "unsupported"


def extract_file_name(key: str) -> str:
    return Path(key).name


def infer_customer_id_from_key(key: str, default_customer_id: str = DEFAULT_CUSTOMER_ID) -> str:
    parts = key.split("/")
    # Expected pattern: input/{env}/{customer_id}/filename
    if len(parts) >= 3:
        # input/dev/evapo/file.pdf
        if parts[0] == "input":
            return parts[2]
    return default_customer_id


def handler(event, context):
    logger.info("Received SQS event: %s", json.dumps(event))

    parsed_records = parse_sqs_wrapped_s3_event(event)
    results = []

    for record in parsed_records:
        bucket = record["bucket"]
        key = record["key"]
        etag = record["etag"]
        customer_id = infer_customer_id_from_key(key)
        source_file_type = detect_file_type(key)
        source_file_name = extract_file_name(key)

        if source_file_type == "unsupported":
            logger.warning("Skipping unsupported file type for key=%s", key)
            results.append(
                {
                    "key": key,
                    "status": "UNSUPPORTED_FILE",
                }
            )
            continue

        doc_id = make_doc_id(APP_ENV, bucket, key, etag, customer_id)

        item = {
            "doc_id": doc_id,
            "environment": APP_ENV,
            "customer_id": customer_id,
            "s3_bucket": bucket,
            "s3_key": key,
            "etag": etag,
            "source_file_type": source_file_type,
            "source_file_name": source_file_name,
            "status": "RECEIVED",
            "ttl": make_ttl(30),
        }

        is_new = try_register_document(item)

        if not is_new:
            logger.info("Duplicate document skipped. doc_id=%s key=%s", doc_id, key)
            results.append(
                {
                    "doc_id": doc_id,
                    "key": key,
                    "status": "DUPLICATE_SKIPPED",
                }
            )
            continue

        logger.info(
            "Registered new document. doc_id=%s customer_id=%s file_type=%s key=%s",
            doc_id,
            customer_id,
            source_file_type,
            key,
        )

        results.append(
            {
                "doc_id": doc_id,
                "key": key,
                "status": "RECEIVED",
            }
        )

    return {
        "statusCode": 200,
        "body": json.dumps(results),
    }