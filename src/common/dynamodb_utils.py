import os

import boto3


def get_dynamodb_table(table_name: str | None = None):
    dynamodb = boto3.resource("dynamodb")
    table_name = table_name or os.getenv("PROCESSED_DOCS_TABLE", "")
    return dynamodb.Table(table_name)