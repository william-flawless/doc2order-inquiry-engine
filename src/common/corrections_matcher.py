import os
import re
from typing import Any

import boto3

# =========================
# AWS resources
# =========================
ddb = boto3.resource("dynamodb")

# =========================
# Corrections config
# =========================
CORRECTIONS_TABLE = os.getenv("CORRECTIONS_TABLE", "Doc2OrderCorrections")
CORRECTIONS_ENABLED = os.getenv("CORRECTIONS_ENABLED", "true").lower() == "true"

# Warm cache per Lambda container
_CORRECTIONS_CACHE: dict[str, dict[str, Any]] = {}

# --- tokenization helpers ---
_WORD_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def _norm_text(s: str) -> str:
    s = (s or "").lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[\r\n\t]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _tokens(s: str) -> list[str]:
    return _WORD_RE.findall(_norm_text(s))


def _extract_discriminators(tokens: list[str]) -> dict[str, str]:
    """
    Extract stable discriminators that commonly define variants.
    Keep conservative + explicit only.
    """
    ts = [t.lower() for t in tokens]
    s = " ".join(ts)

    out: dict[str, str] = {}

    # 10k / 10000 etc. Normalize "10k" to "10000"
    if "10k" in ts:
        out["puffs"] = "10000"
    if "6k" in ts:
        out["puffs"] = "6000"

    # raw numeric puffs like 6000/10000/12000/15000 etc
    m = re.search(r"\b(6000|8000|9000|10000|11000|12000|15000|20000|25000)\b", s)
    if m:
        out["puffs"] = m.group(1)

    # COREX marker (Xros)
    if "corex" in ts:
        out["corex"] = "1"

    # GO marker (Xlim/Nexlim Go)
    if "nexlim" in ts and "go" in ts:
        out["go"] = "1"

    # V3 / V2 / V4 (pods)
    mv = re.search(r"\bv([2-9])\b", s)
    if mv:
        out["ver"] = f"v{mv.group(1)}"

    # Product type: pods vs kit (explicit only)
    if "pod" in ts or "pods" in ts:
        out["type"] = "pods"
    if "kit" in ts or "device" in ts:
        out["type2"] = "kit"

    return out


def _extract_brand_base(tokens: list[str]) -> tuple[str, str]:
    """
    Produce (brand, base_family) in a minimal-risk way.
    We intentionally keep this small to avoid cross-product collisions.
    """
    ts = [t.lower() for t in tokens]
    tset = set(ts)

    brand = ""
    base = ""

    if "dojo" in tset:
        brand = "vaporesso"
        if "pod" in tset or "pods" in tset:
            base = "dojo_pods"
        elif "kit" in tset:
            base = "kit"
        else:
            base = "dojo"

    elif "xros" in tset:
        brand = "vaporesso"
        base = "xros"

    elif "xlim" in tset or "xlm" in tset:
        brand = "oxva"
        base = "xlim"

    elif "nexlim" in tset:
        brand = "oxva"
        base = "nexlim"

    else:
        # fallback: first 2 meaningful tokens (conservative)
        if len(ts) >= 1:
            brand = ts[0]
        if len(ts) >= 2:
            base = ts[1]
        else:
            base = brand

    return brand, base


def build_sku_only_signature(customer_sku: str | None) -> str | None:
    if not customer_sku:
        return None
    cs = _norm_text(customer_sku)
    cs = re.sub(r"\s+", "", cs)
    cs = re.sub(r"[^a-z0-9\\-]+", "", cs)
    if not cs:
        return None
    return f"sku={cs}"


def build_correction_signature(description: str, customer_sku: str | None = None) -> str:
    """
    Signature format (stable & comparable):
      brand=<...>|base=<...>|disc:k=v,k=v|sku=<...optional>
    - We include sku ONLY if explicitly present (strongest identifier).
    """
    toks = _tokens(description)
    brand, base = _extract_brand_base(toks)
    disc = _extract_discriminators(toks)

    disc_part = ",".join([f"{k}={disc[k]}" for k in sorted(disc.keys())]) if disc else ""

    parts = [
        f"brand={brand}" if brand else "brand=",
        f"base={base}" if base else "base=",
        f"disc:{disc_part}" if disc_part else "disc:",
    ]

    if customer_sku:
        cs = _norm_text(customer_sku).replace(" ", "")
        if cs:
            parts.append(f"sku={cs}")

    return "|".join(parts)


def get_correction(customer_id: str, signature: str) -> dict[str, Any] | None:
    """
    Lookup correction by (customer_id + signature).
    Uses warm cache per Lambda container.
    """
    if not CORRECTIONS_ENABLED:
        return None

    customer_id = (customer_id or "").strip()
    signature = (signature or "").strip()
    if not customer_id or not signature:
        return None

    cache_key = f"{customer_id}::{signature}"
    if cache_key in _CORRECTIONS_CACHE:
        return _CORRECTIONS_CACHE[cache_key] or None

    table = ddb.Table(CORRECTIONS_TABLE)
    pk = f"CUST#{customer_id}"
    sk = f"SIG#{signature}"

    resp = table.get_item(Key={"pk": pk, "sk": sk})
    item = resp.get("Item")

    if item and item.get("enabled") is False:
        item = None

    _CORRECTIONS_CACHE[cache_key] = item or {}
    return item or None