from typing import Any

from src.common.corrections_matcher import (
    build_correction_signature,
    build_sku_only_signature,
    get_correction,
)


def run_evapo_deterministic_precheck(
    customer_id: str,
    line_items: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """
    line_items expected shape:
    [
        {
            "row_index": 2,
            "description": "Crystal 600 Pro Kit Cherry Ice",
            "quantity": 20,
            "customer_sku": "22625",
            "raw_row_data": {...}
        }
    ]
    """
    matched_rows: list[dict[str, Any]] = []
    unresolved_rows: list[dict[str, Any]] = []

    for item in line_items:
        row_index = item.get("row_index")
        description = (item.get("description") or "").strip()
        customer_sku = (item.get("customer_sku") or "").strip()

        correction = None
        matched_signature = None

        # 1) SKU-only signature
        sig_sku = build_sku_only_signature(customer_sku)
        if sig_sku:
            correction = get_correction(customer_id, sig_sku)
            if correction:
                matched_signature = sig_sku

        # 2) Composite signature
        if not correction:
            sig_full = build_correction_signature(description, customer_sku)
            correction = get_correction(customer_id, sig_full)
            if correction:
                matched_signature = sig_full

        if correction:
            matched_rows.append(
                {
                    **item,
                    "match_status": "DETERMINISTIC_MATCHED",
                    "matched_signature": matched_signature,
                    "correction_record": correction,
                }
            )
        else:
            unresolved_rows.append(
                {
                    **item,
                    "match_status": "UNRESOLVED",
                    "matched_signature": None,
                    "correction_record": None,
                }
            )

    return {
        "matched_rows": matched_rows,
        "unresolved_rows": unresolved_rows,
    }