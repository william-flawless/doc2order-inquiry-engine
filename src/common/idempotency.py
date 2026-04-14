import time
from typing import Any, Dict

from botocore.exceptions import ClientError

from src.common.dynamodb_utils import get_dynamodb_table


def make_ttl(days: int = 30) -> int:
    return int(time.time()) + days * 24 * 60 * 60


def try_register_document(item: Dict[str, Any], table_name: str | None = None) -> bool:
    table = get_dynamodb_table(table_name)

    try:
        table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(doc_id)",
        )
        return True
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code")
        if error_code == "ConditionalCheckFailedException":
            return False
        raise