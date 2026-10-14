class InvoiceExtractor:
    @classmethod
    def get_invoice_fields(cls):
        return {
            "invoice_number":None,
            "invoice_date":None,
            "due_date":None,
            "Payment_terms":None,
            "Company_code":None,
            "vendor_address":None,
            "vendor_tax_id":None,
            "vendor_bank_name":None,
            "vendor_account_no":None,
            "vendor_sort_code":None,
            "vendor_iban":None,
            "customer_name":None,
            "customer_address":None,
            "po_number":None,
            "reference_number":None,
            "currency":None,
            "subtotal":None,
            "tax_percentage":None,
            "total_amount":None,
        }

    @classmethod
    def get_invoice_item_field(cls):
        return{
            "line_no":None,
            "description":None,
            "quantity":None,
            "unit_price":None,
            "amount":None,
            "tax_percent":None,
            "reference_code":None,

        }

    @classmethod
    def get_additional_fields(cls):
        return{
            "field_name":None,
            "field_value":None
        }

    @classmethod
    def get_invoice_structure(cls):
        return {
            "invoice_header":cls.get_invoice_fields(),
            "line_item":[
                cls.get_invoice_item_field()
            ],
            "additional_fields":[
                cls.get_additional_fields()
            ],
        }

# invoice_data=InvoiceExtractor.get_invoice_structure