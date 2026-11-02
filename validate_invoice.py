from extractor.schema import InvoiceData

sample = {
    "invoice_number": "INV-2026-0417",
    "invoice_date": "2026-03-14",
    "vendor_name": "Brightwater Supplies Ltd",
    "customer_name": "Demo Customer Co",
    "subtotal": 17900.0,
    "tax": 3222.0,
    "total": 21122.0,
}

invoice = InvoiceData.model_validate(sample)

print("Invoice validation successful!")
print(invoice.model_dump_json(indent=2))
