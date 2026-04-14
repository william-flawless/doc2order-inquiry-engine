import hashlib


def make_doc_id(environment: str, bucket: str, key: str, etag: str, customer_id: str) -> str:
    raw = f"{environment}|{bucket}|{key}|{etag}|{customer_id}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()