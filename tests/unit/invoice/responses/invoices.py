true, false, null = True, False, None

invoice_response_ok = {
    "InvoiceArray": {
        "Invoice": [
            {
                "invoiceNumber": "INV-2024-001",
                "invoiceType": "INVOICE",
                "invoiceDate": "2024-08-15",
                "purchaseOrderNumber": "PO-12345",
                "purchaseOrderVersion": "1",
                "BillTo": {
                    "AccountInfo": {
                        "accountName": "Acme Corp",
                        "accountNumber": "ACCT-100",
                        "attentionTo": "John Doe",
                        "Address1": "123 Main St",
                        "Address2": "Suite 400",
                        "Address3": "Building B",
                        "city": "New York",
                        "region": "NY",
                        "postalCode": "10001",
                        "country": "US",
                        "email": "john@acme.com",
                        "phone": "212-555-1234"
                    }
                },
                "SoldTo": {
                    "AccountInfo": {
                        "accountName": "Acme West",
                        "accountNumber": "ACCT-200",
                        "attentionTo": "Jane Smith",
                        "Address1": "456 Oak Ave",
                        "Address2": null,
                        "Address3": null,
                        "city": "Los Angeles",
                        "region": "CA",
                        "postalCode": "90001",
                        "country": "US",
                        "email": "jane@acmewest.com",
                        "phone": "310-555-5678"
                    }
                },
                "invoiceComments": "Net 30 terms apply",
                "paymentTerms": "Net 30",
                "paymentDueDate": "2024-09-14",
                "currency": "USD",
                "fob": "Origin",
                "salesAmount": 500.00,
                "shippingAmount": 25.00,
                "handlingAmount": 5.00,
                "taxAmount": 42.40,
                "invoiceAmount": 572.40,
                "advancePaymentAmount": 0.00,
                "invoiceAmountDue": 572.40,
                "invoiceDocumentUrl": "https://example.com/invoices/INV-2024-001.pdf",
                "InvoiceLineItemsArray": {
                    "InvoiceLineItem": [
                        {
                            "invoiceLineItemNumber": 1.0,
                            "productId": "PROD-100",
                            "partId": "PART-100-BLK",
                            "chargeId": "CHG-001",
                            "purchaseOrderLineItemNumber": "1",
                            "orderedQuantity": 100.0,
                            "invoiceQuantity": 100.0,
                            "backOrderedQuantity": 0.0,
                            "quantityUOM": "EA",
                            "lineItemDescription": "Custom Widget - Black",
                            "unitPrice": 5.00,
                            "discountAmount": 0.00,
                            "extendedPrice": 500.00,
                            "distributorProductId": "DIST-PROD-100",
                            "distributorPartId": "DIST-PART-100-BLK"
                        }
                    ]
                },
                "SalesOrderNumbersArray": {
                    "SalesOrderNumber": [
                        {"salesOrderNumber": "SO-9001"},
                        {"salesOrderNumber": "SO-9002"}
                    ]
                },
                "TaxArray": {
                    "tax": [
                        {
                            "taxType": "SALES",
                            "taxJurisdiction": "NY",
                            "taxAmount": 40.00
                        },
                        {
                            "taxType": "SALES",
                            "taxJurisdiction": "NYC",
                            "taxAmount": 2.40
                        }
                    ]
                },
                "invoicePaymentUrl": "https://example.com/pay/INV-2024-001"
            },
            {
                "invoiceNumber": "INV-2024-002",
                "invoiceType": "INVOICE",
                "invoiceDate": "2024-08-16",
                "purchaseOrderNumber": "PO-12346",
                "purchaseOrderVersion": null,
                "BillTo": null,
                "SoldTo": null,
                "invoiceComments": null,
                "paymentTerms": null,
                "paymentDueDate": "2024-09-15",
                "currency": "USD",
                "fob": null,
                "salesAmount": 200.00,
                "shippingAmount": 10.00,
                "handlingAmount": 0.00,
                "taxAmount": 0.00,
                "invoiceAmount": 210.00,
                "advancePaymentAmount": 0.00,
                "invoiceAmountDue": 210.00,
                "invoiceDocumentUrl": null,
                "InvoiceLineItemsArray": {
                    "InvoiceLineItem": [
                        {
                            "invoiceLineItemNumber": 1.0,
                            "productId": "PROD-200",
                            "partId": "PART-200-WHT",
                            "chargeId": "CHG-002",
                            "purchaseOrderLineItemNumber": "1",
                            "orderedQuantity": 50.0,
                            "invoiceQuantity": 50.0,
                            "backOrderedQuantity": null,
                            "quantityUOM": "EA",
                            "lineItemDescription": "Standard Gadget - White",
                            "unitPrice": 4.00,
                            "discountAmount": null,
                            "extendedPrice": 200.00,
                            "distributorProductId": null,
                            "distributorPartId": null
                        }
                    ]
                },
                "SalesOrderNumbersArray": null,
                "TaxArray": null,
                "invoicePaymentUrl": null
            }
        ]
    },
    "ServiceMessageArray": null
}
