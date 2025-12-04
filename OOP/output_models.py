class ProductOutputModel:
    """Formats product data for output"""
    
    def __init__(self, product):
        self.stock_code = product.stock_code
        self.description = product.description
        self.unit_price = product.unit_price
    
    def to_dict(self):
        return {
            'stock_code': self.stock_code,
            'description': self.description,
            'unit_price': self.unit_price
        }


class InvoiceOutputModel:
    """Formats invoice data for output"""
    
    def __init__(self, invoice):
        self.invoice_number = invoice.invoice_no
        self.invoice_date = invoice.invoice_date
        self.total_amount = round(invoice.get_invoice_total(), 2)
        self.items = invoice.get_items_with_subtotals()
    
    def to_dict(self):
        return {
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date,
            'total_amount': self.total_amount,
            'items': [
                {
                    'product': item['product'],
                    'quantity': item['quantity'],
                    'unit_price': round(item['unit_price'], 2),
                    'subtotal': round(item['subtotal'], 2)
                }
                for item in self.items
            ]
        }


class CustomerOutputModel:
    """Formats customer data for output"""
    
    def __init__(self, customer):
        self.customer_id = customer.customer_id
        self.country = customer.country
        self.total_spent = round(customer.total_spent, 2)
    
    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'country': self.country,
            'total_spent': self.total_spent
        }


class CustomerSummaryOutputModel:
    """Formats a summary of all customers"""
    
    def __init__(self, customers_dict):
        self.total_customers = len(customers_dict)
        self.customers = [
            CustomerOutputModel(customer).to_dict() 
            for customer in customers_dict.values()
        ]
    
    def to_dict(self):
        return {
            'total_customers': self.total_customers,
            'customers': self.customers
        }


class InvoiceSummaryOutputModel:
    """Formats a summary of all invoices"""
    
    def __init__(self, invoices_dict):
        self.total_invoices = len(invoices_dict)
        total_revenue = sum(invoice.get_invoice_total() for invoice in invoices_dict.values())
        self.total_revenue = round(total_revenue, 2)
        self.invoices = [
            InvoiceOutputModel(invoice).to_dict() 
            for invoice in invoices_dict.values()
        ]
    
    def to_dict(self):
        return {
            'total_invoices': self.total_invoices,
            'total_revenue': self.total_revenue,
            'invoices': self.invoices
        }


class ProductCatalogOutputModel:
    """Formats a catalog of all products"""
    
    def __init__(self, products_dict):
        self.total_products = len(products_dict)
        self.products = [
            ProductOutputModel(product).to_dict() 
            for product in products_dict.values()
        ]
    
    def to_dict(self):
        return {
            'total_products': self.total_products,
            'products': self.products
        }


class CustomersByCountryOutputModel:
    """Groups and formats customers by country"""
    
    def __init__(self, customers_dict):
        countries = {}
        for customer in customers_dict.values():
            country = customer.country
            if country not in countries:
                countries[country] = []
            countries[country].append(CustomerOutputModel(customer).to_dict())
        
        self.countries = countries
        self.total_countries = len(countries)
    
    def to_dict(self):
        return {
            'total_countries': self.total_countries,
            'customers_by_country': self.countries
        }