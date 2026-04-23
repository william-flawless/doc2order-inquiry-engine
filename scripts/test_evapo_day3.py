from pathlib import Path
import sys
from pprint import pprint

# Add repo root to Python path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.core.normalize.evapo_stock_inquiry_transformer import transform_evapo_rows_to_line_items
from src.core.parsers.xlsx.evapo_stock_inquiry_parser import parse_evapo_stock_inquiry_workbook


def main():
    bucket = "flawless-doc2order-inquiry-engine-prod"
    key = "input/dev/evapo/Stock Enquiry Pre-Filled 120326.xlsx"

    parsed = parse_evapo_stock_inquiry_workbook(bucket=bucket, key=key)
    line_items = transform_evapo_rows_to_line_items(parsed["raw_rows"])

    print("Sheet:", parsed["sheet_name"])
    print("Header map:")
    pprint(parsed["header_map"])

    print("\nFirst 5 raw rows:")
    pprint(parsed["raw_rows"][:5])

    print("\nFirst 5 line items:")
    pprint(line_items[:5])


if __name__ == "__main__":
    main()