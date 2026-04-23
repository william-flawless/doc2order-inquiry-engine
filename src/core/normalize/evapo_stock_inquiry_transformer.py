from __future__ import annotations

from typing import Any


def _clean_str(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    return text if text else None


def _coerce_quantity(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if not text:
        return None

    try:
        return float(text.replace(",", ""))
    except ValueError:
        return None


def _build_description(raw_row_data: dict[str, Any]) -> str:
    """
    Keep Day 3 behavior aligned to your existing app.py logic:
    use the workbook Description column as the primary description string
    for deterministic corrections matching.

    Do NOT combine Brand/Category here unless you intentionally want to
    change the signature behavior versus the existing order-processing lambda.
    """
    description = _clean_str(raw_row_data.get("Description"))
    return description or ""


def transform_evapo_row_to_line_item(
    row_index: int,
    raw_row_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Convert one Evapo workbook row into a matcher-compatible structure.

    Output shape:
    {
      "row_index": 2,
      "description": "Crystal 600 Pro Kit Cherry Ice",
      "quantity": 20.0,
      "customer_sku": "22625",
      "raw_row_data": {...}
    }
    """
    customer_sku = _clean_str(raw_row_data.get("Sku"))
    description = _build_description(raw_row_data)
    quantity = _coerce_quantity(raw_row_data.get("Qty"))

    return {
        "row_index": row_index,
        "description": description,
        "quantity": quantity,
        "customer_sku": customer_sku,
        "raw_row_data": raw_row_data,
    }


def transform_evapo_rows_to_line_items(
    raw_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Convert all extracted raw rows into line items ready for deterministic precheck.
    """
    line_items: list[dict[str, Any]] = []

    for row in raw_rows:
        row_index = row["row_index"]
        raw_row_data = row["raw_row_data"]

        line_item = transform_evapo_row_to_line_item(
            row_index=row_index,
            raw_row_data=raw_row_data,
        )
        line_items.append(line_item)

    return line_items