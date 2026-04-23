# Evapo Workbook Contract

## Expected file type
- .xlsx

## Required columns
- Sku: This is evapo's SKU which is different from our internal SKU; it should be passed into the matching system as customer_sku
- Category: This specificies the type of product like Pod Kit, Pod Pack, etc
- Brand: This shows the brand of the product
- Description: This shows the description of the product
- Qty: Quantity of the product
- Stock: To be filled after matching
- Price: To be filled after matching

## Input columns used for matching
- Sku
- Brand
- Description
- Category

## Output columns reserved for enrichment
- Stock
- Price

## Expected behavior
- preserve row order
- preserve workbook shape
- fill Stock and Price later