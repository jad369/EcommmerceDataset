"""CSV data processor"""

import csv
from models import Product, Invoice, Customer
from mappers import ProductMapper, InvoiceMapper, CustomerMapper


class CSVDataProcessor:
    """Main class to process CSV data and create domain objects"""
    
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        self.products = {}
        self.invoices = {}
        self.customers = {}
    
    def load_data(self):
        """Load and process the CSV file"""
        try:
            file = open(self.csv_filename, 'r', encoding='utf-8')
            reader = csv.reader(file)
            
            next(reader)
            
            row_count = 0
            for row in reader:
                self._process_row(row)
                row_count += 1
            
            file.close()
            
            print(f" Successfully processed {row_count} rows")
            print(f"   - Products: {len(self.products)}")
            print(f"   - Invoices: {len(self.invoices)}")
            print(f"   - Customers: {len(self.customers)}")
            
        except FileNotFoundError:
            print(f" ERROR: File '{self.csv_filename}' not found")
            print("   Make sure the file is in the same folder as this script")
        except IndexError as e:
            print(f" ERROR: CSV file has wrong structure - {e}")
            print("   Check that your CSV has the correct columns")
        except Exception as e:
            print(f" ERROR: {e}")
    
    def _process_row(self, row):
        """Process a single CSV row (private method)"""
        invoice_no = row[0]
        stock_code = row[1]
        customer_id = row[6]
        
        if stock_code not in self.products:
            self.products[stock_code] = ProductMapper.from_csv_row(row)
        
        if invoice_no not in self.invoices:
            self.invoices[invoice_no] = InvoiceMapper.from_csv_row(row)
        InvoiceMapper.add_item_from_csv_row(self.invoices[invoice_no], row)
        
        if customer_id not in self.customers:
            self.customers[customer_id] = CustomerMapper.from_csv_row(row)
        CustomerMapper.add_purchase_from_csv_row(self.customers[customer_id], row)
    
    def get_product(self, stock_code):
        return self.products.get(stock_code)
    
    def get_invoice(self, invoice_no):
        return self.invoices.get(invoice_no)
    
    def get_customer(self, customer_id):
        return self.customers.get(customer_id)
    
    def get_all_products(self):
        return self.products
    
    def get_all_invoices(self):
        return self.invoices
    
    def get_all_customers(self):
        return self.customers
    
    def get_product_catalog(self):
        return ProductMapper.collection_to_catalog(self.products)
    
    def get_invoice_summary(self):
        return InvoiceMapper.collection_to_summary(self.invoices)
    
    def get_customer_summary(self):
        return CustomerMapper.collection_to_summary(self.customers)
    
    def get_customers_by_country(self):
        return CustomerMapper.group_by_country(self.customers)
    
    def get_total_revenue(self):
        total = 0
        for invoice in self.invoices.values():
            total += invoice.get_invoice_total()
        return total
    
    def get_top_customers(self, limit=10):
        def get_customer_spending(customer):
            return customer.total_spent
        
        customers_list = list(self.customers.values())
        sorted_customers = sorted(customers_list, key=get_customer_spending, reverse=True)
        return sorted_customers[:limit]
    
    def search_products(self, search_term):
        results = []
        search_upper = search_term.upper()
        
        for product in self.products.values():
            if search_upper in product.description.upper():
                results.append(product)
        
        return results
    
    def get_high_value_invoices(self, threshold=1000):
        high_value = []
        
        for invoice in self.invoices.values():
            if invoice.total > threshold:
                high_value.append(invoice)
        
        def get_invoice_total(invoice):
            return invoice.total
        
        return sorted(high_value, key=get_invoice_total, reverse=True)