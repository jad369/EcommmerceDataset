#Output Models

class ProductOutputModel:
    """Output model for Product data"""
    
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
    """Output model for Invoice data"""
    
    def __init__(self, invoice):
        self.invoice_number = invoice.invoice_no
        self.invoice_date = invoice.invoice_date
        self.main_product = invoice.main_product
        self.main_quantity = invoice.main_quantity
        self.total_amount = round(invoice.get_invoice_total(), 2)
        self.item_count = invoice.get_item_count()
        self.total_quantity = invoice.get_total_quantity()
        self.items = invoice.get_items_with_subtotals()
    
    def to_dict(self):
        converted_items = []
        for item in self.items:
            converted_item = {
                'product': item['product'],
                'quantity': item['quantity'],
                'unit_price': round(item['unit_price'], 2),
                'subtotal': round(item['subtotal'], 2)
            }
            converted_items.append(converted_item)
        
        return {
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date,
            'main_product': self.main_product,
            'main_quantity': self.main_quantity,
            'total_amount': self.total_amount,
            'item_count': self.item_count,
            'total_quantity': self.total_quantity,
            'items': converted_items
        }


class CustomerOutputModel:
    """Output model for Customer data"""
    
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
    """Output model for all customers summary"""
    
    def __init__(self, customers_dict):
        self.total_customers = len(customers_dict)
        
        self.customers = []
        for customer in customers_dict.values():
            customer_output = CustomerOutputModel(customer)
            self.customers.append(customer_output.to_dict())
    
    def to_dict(self):
        return {
            'total_customers': self.total_customers,
            'customers': self.customers
        }


class InvoiceSummaryOutputModel:
    """Output model for all invoices summary"""
    
    def __init__(self, invoices_dict):
        self.total_invoices = len(invoices_dict)
        
        total_revenue = 0
        for invoice in invoices_dict.values():
            total_revenue += invoice.get_invoice_total()
        self.total_revenue = round(total_revenue, 2)
        
        self.invoices = []
        for invoice in invoices_dict.values():
            invoice_output = InvoiceOutputModel(invoice)
            self.invoices.append(invoice_output.to_dict())
    
    def to_dict(self):
        return {
            'total_invoices': self.total_invoices,
            'total_revenue': self.total_revenue,
            'invoices': self.invoices
        }


class ProductCatalogOutputModel:
    """Output model for product catalog"""
    
    def __init__(self, products_dict):
        self.total_products = len(products_dict)
        
        self.products = []
        for product in products_dict.values():
            product_output = ProductOutputModel(product)
            self.products.append(product_output.to_dict())
    
    def to_dict(self):
        return {
            'total_products': self.total_products,
            'products': self.products
        }


class CustomersByCountryOutputModel:
    """Output model for customers grouped by country"""
    
    def __init__(self, customers_dict):
        countries = {}
        for customer in customers_dict.values():
            country = customer.country
            if country not in countries:
                countries[country] = []
            
            customer_output = CustomerOutputModel(customer)
            countries[country].append(customer_output.to_dict())
        
        self.countries = countries
        self.total_countries = len(countries)
    
    def to_dict(self):
        return {
            'total_countries': self.total_countries,
            'customers_by_country': self.countries
        }