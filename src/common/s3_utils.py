import json
from io import BytesIO
from typing import Any

import boto3

s3_client = boto3.client("s3")


def get_object_bytes(bucket: str, key: str) -> bytes:
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


def put_json(bucket: str, key: str, payload: Any) -> None:
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType="application/json",
    )


def get_object_bytes_io(bucket: str, key: str) -> BytesIO:
    return BytesIO(get_object_bytes(bucket, key))