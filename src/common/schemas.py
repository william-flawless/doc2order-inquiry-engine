from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ProcessingContext:
    environment: str
    customer_id: str
    bucket: str
    key: str
    etag: str
    doc_id: str
    source_file_type: str


@dataclass
class NormalizedRow:
    row_id: str
    doc_id: str
    customer_id: str
    source_file_name: str
    source_file_type: str
    source_sheet_name: Optional[str]
    source_page_number: Optional[int]
    customer_product_description: str
    requested_quantity: Optional[float]
    requested_uom: Optional[str]
    raw_row_data: Dict[str, Any]
    extraction_method: str
    parser_version: str
    normalization_warnings: List[str] = field(default_factory=list)