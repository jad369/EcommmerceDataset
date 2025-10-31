#OOP
import csv

class Product:
    
    def __init__(self, stock_code, description, unit_price): 
        self.stock_code = stock_code
        self.description = description
        self.unit_price = unit_price
    
    def show(self):
        print(f"{self.stock_code}: {self.description} (sold {self.unit_price} times)")


class Invoice:
    
    def __init__(self, invoice_no, invoice_date, product, quantity):
        self.invoice_no = invoice_no
        self.invoice_date = invoice_date
        self.product = product
        self.quantity = quantity
        self.total = 0
        self.items = []
    
    def get_total(self, quantity, price):
        sale = quantity * price
        self.total = self.total + sale
    
    def add_item(self, product, quantity, price):
        """Add an item to the invoice with its subtotal"""
        subtotal = quantity * price
        self.items.append({
            'product': product,
            'quantity': quantity,
            'unit_price': price,
            'subtotal': subtotal
        })
        self.total += subtotal
    
    def get_invoice_total(self):
        """Get the invoice total"""
        return self.total
    
    def get_items_with_subtotals(self):
        """Get all invoice items with their subtotals"""
        return self.items
    
    def show(self):
        print(f"Invoice {self.invoice_no}: ${self.total}")
        print("Items:")
        for item in self.items:
            print(f"  - {item['product']}: {item['quantity']} x ${item['unit_price']:.2f} = ${item['subtotal']:.2f}")


class Customer:
    
    def __init__(self, customer_id, country):
        self.customer_id = customer_id
        self.country = country
        self.total_spent = 0
    
    def add_purchase(self, amount):
        """Add a purchase amount to customer's total"""
        self.total_spent += amount
    
    def show(self):
        print(f"Customer {self.customer_id} from {self.country} spent: ${self.total_spent:.2f}")


# ========== OUTPUT MODELS ==========

class ProductOutputModel:
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


#Mapping Functions

def csv_row_to_product(row):
    """Turn a CSV row into a Product object"""
    stock_code = row[1]
    description = row[2]
    price = float(row[5])
    return Product(stock_code, description, price)


def csv_row_to_invoice(row):
    """Turn a CSV row into an Invoice object"""
    invoice_no = row[0]
    invoice_date = row[4]
    return Invoice(invoice_no, invoice_date, None, None)


def csv_row_to_customer(row):
    """Turn a CSV row into a Customer object"""
    customer_id = row[6]
    country = row[7]
    return Customer(customer_id, country)


def product_to_dict(product):
    """Turn a Product into a dictionary"""
    return {
        'stock_code': product.stock_code,
        'description': product.description,
        'unit_price': product.unit_price
    }


def invoice_to_dict(invoice):
    """Turn an Invoice into a dictionary"""
    return {
        'invoice_number': invoice.invoice_no,
        'invoice_date': invoice.invoice_date,
        'total': round(invoice.total, 2),
        'items': invoice.items
    }


def customer_to_dict(customer):
    """Turn a Customer into a dictionary"""
    return {
        'customer_id': customer.customer_id,
        'country': customer.country,
        'total_spent': round(customer.total_spent, 2)
    }


def all_products_to_dict(products_dict):
    """Turn all products into a list of dictionaries"""
    result = []
    for product in products_dict.values():
        result.append(product_to_dict(product))
    return result


def all_customers_to_dict(customers_dict):
    """Turn all customers into a list of dictionaries"""
    result = []
    for customer in customers_dict.values():
        result.append(customer_to_dict(customer))
    return result


def all_invoices_to_dict(invoices_dict):
    """Turn all invoices into a list of dictionaries"""
    result = []
    for invoice in invoices_dict.values():
        result.append(invoice_to_dict(invoice))
    return result


def customers_by_country(customers_dict):
    """Group customers by their country"""
    countries = {}
    for customer in customers_dict.values():
        country = customer.country
        if country not in countries:
            countries[country] = []
        countries[country].append(customer_to_dict(customer))
    return countries

file = open('final_dataset.csv', 'r')
reader = csv.reader(file)

next(reader)

products = {}
invoices = {}
customers = {}

for row in reader:
    invoice_no = row[0]
    stock_code = row[1]
    description = row[2]
    quantity = int(row[3])
    price = float(row[5])
    customer_id = row[6]
    
    if stock_code not in products:
        products[stock_code] = csv_row_to_product(row)
    
    if invoice_no not in invoices:
        invoices[invoice_no] = csv_row_to_invoice(row)
    invoices[invoice_no].add_item(description, quantity, price)
    
    if customer_id not in customers:
        customers[customer_id] = csv_row_to_customer(row)
    customers[customer_id].add_purchase(quantity * price)

file.close()
