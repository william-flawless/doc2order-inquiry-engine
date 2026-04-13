import json

from src.common.logging_utils import get_logger

logger = get_logger(__name__)


def handler(event, context):
    logger.info("Received event: %s", json.dumps(event))
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "placeholder"})
    }