import json
from typing import Any, Dict, List


def parse_sqs_wrapped_s3_event(event: Dict[str, Any]) -> List[Dict[str, str]]:
    records_out = []

    for sqs_record in event.get("Records", []):
        body = sqs_record.get("body", "{}")
        s3_event = json.loads(body)

        for s3_record in s3_event.get("Records", []):
            bucket = s3_record["s3"]["bucket"]["name"]
            key = s3_record["s3"]["object"]["key"]
            etag = s3_record["s3"]["object"].get("eTag") or s3_record["s3"]["object"].get("etag", "")

            records_out.append(
                {
                    "bucket": bucket,
                    "key": key,
                    "etag": etag,
                }
            )

    return records_out