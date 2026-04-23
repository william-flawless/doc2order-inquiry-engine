import os
from functools import lru_cache
from typing import Any, Dict

import yaml


class CustomerConfigError(Exception):
    """Base exception for customer config issues."""
    pass


class CustomerConfigNotFoundError(CustomerConfigError):
    """Raised when customer config file is missing."""
    pass


class CustomerConfigInvalidError(CustomerConfigError):
    """Raised when config file is invalid or malformed."""
    pass


def _get_config_path(customer_id: str) -> str:
    """
    Build the absolute path to the customer config.yaml file.

    Expected structure:
    src/customers/{customer_id}/config.yaml
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(
        base_dir,
        "customers",
        customer_id,
        "config.yaml",
    )
    return config_path


@lru_cache(maxsize=32)
def load_customer_config(customer_id: str) -> Dict[str, Any]:
    """
    Load and cache the customer configuration from YAML.

    Args:
        customer_id (str): customer identifier (e.g., "evapo")

    Returns:
        Dict[str, Any]: parsed config

    Raises:
        CustomerConfigNotFoundError
        CustomerConfigInvalidError
    """
    if not customer_id:
        raise CustomerConfigInvalidError("customer_id is required")

    config_path = _get_config_path(customer_id)

    if not os.path.exists(config_path):
        raise CustomerConfigNotFoundError(
            f"Config file not found for customer '{customer_id}' at path: {config_path}"
        )

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as exc:
        raise CustomerConfigInvalidError(
            f"Failed to load YAML config for customer '{customer_id}': {str(exc)}"
        ) from exc

    if not isinstance(config, dict):
        raise CustomerConfigInvalidError(
            f"Config for customer '{customer_id}' must be a dictionary"
        )

    # Basic validation (minimal but important)
    required_top_level_keys = ["customer_id"]

    for key in required_top_level_keys:
        if key not in config:
            raise CustomerConfigInvalidError(
                f"Missing required key '{key}' in config for customer '{customer_id}'"
            )

    return config


def get_customer_config(customer_id: str) -> Dict[str, Any]:
    """
    Public accessor for customer config.

    This wraps the cached loader and can later be extended
    with additional logic if needed.

    Args:
        customer_id (str)

    Returns:
        Dict[str, Any]
    """
    return load_customer_config(customer_id)


def get_nested(config: Dict[str, Any], path: str, default: Any = None) -> Any:
    """
    Safely retrieve nested config values using dot notation.

    Example:
        get_nested(config, "workbook.header_row_index")

    Args:
        config (dict)
        path (str): dot-separated path
        default (Any)

    Returns:
        Any
    """
    keys = path.split(".")
    value = config

    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]

    return value