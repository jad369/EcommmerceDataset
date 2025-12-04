import csv
from product import Product
from invoice import Invoice
from customer import Customer
from output_models import CustomersByCountryOutputModel


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
            
            print(f"Successfully processed {row_count} rows")
            print(f"   - Products: {len(self.products)}")
            print(f"   - Invoices: {len(self.invoices)}")
            print(f"   - Customers: {len(self.customers)}")
            
        except FileNotFoundError:
            print(f"ERROR: File '{self.csv_filename}' not found")
            print("   Make sure the file is in the same folder as this script")
        except IndexError as e:
            print(f"ERROR: CSV file has wrong structure - {e}")
            print("   Check that your CSV has the correct columns")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def _process_row(self, row):
        """Process a single CSV row (private method)"""
        # Skip rows that don't have enough columns
        if len(row) < 8:
            return
        
        invoice_no = row[0]
        stock_code = row[1]
        description = row[2]
        
        # Skip rows with missing critical data
        if not invoice_no or not stock_code or not row[3] or not row[5]:
            return
        
        try:
            quantity = int(row[3])
            price = float(row[5])
        except (ValueError, IndexError):
            return  # Skip rows with invalid numeric data
        
        customer_id = row[6] if row[6] else "UNKNOWN"
        country = row[7] if row[7] else "UNKNOWN"
        invoice_date = row[4]
        
        # Create or get product
        if stock_code not in self.products:
            self.products[stock_code] = Product(stock_code, description, price)
        
        # Create or get invoice and add item
        if invoice_no not in self.invoices:
            self.invoices[invoice_no] = Invoice(invoice_no, invoice_date, customer_id, country)
        self.invoices[invoice_no].add_item(description, quantity, price)
        
        # Create or get customer and add purchase
        if customer_id not in self.customers:
            self.customers[customer_id] = Customer(customer_id, country)
        self.customers[customer_id].add_purchase(quantity * price)
    
    def get_product(self, stock_code):
        """Get a specific product by stock code"""
        return self.products.get(stock_code)
    
    def get_invoice(self, invoice_no):
        """Get a specific invoice by invoice number"""
        return self.invoices.get(invoice_no)
    
    def get_customer(self, customer_id):
        """Get a specific customer by customer ID"""
        return self.customers.get(customer_id)
    
    def get_all_products(self):
        """Get all products"""
        return self.products
    
    def get_all_invoices(self):
        """Get all invoices"""
        return self.invoices
    
    def get_all_customers(self):
        """Get all customers"""
        return self.customers
    
    def get_total_revenue(self):
        """Calculate total revenue from all invoices"""
        total = 0
        for invoice in self.invoices.values():
            total += invoice.get_invoice_total()
        return total
    
    def get_top_customers(self, limit=10):
        """Get top customers by spending"""
        def get_customer_spending(customer):
            return customer.total_spent
        
        customers_list = list(self.customers.values())
        sorted_customers = sorted(customers_list, key=get_customer_spending, reverse=True)
        return sorted_customers[:limit]
    
    def search_products(self, search_term):
        """Search for products by description"""
        results = []
        search_upper = search_term.upper()
        
        for product in self.products.values():
            if search_upper in product.description.upper():
                results.append(product)
        
        return results
    
    def get_high_value_invoices(self, threshold=1000):
        """Get invoices above a certain value threshold"""
        high_value = []
        
        for invoice in self.invoices.values():
            if invoice.total > threshold:
                high_value.append(invoice)
        
        def get_invoice_total(invoice):
            return invoice.total
        
        return sorted(high_value, key=get_invoice_total, reverse=True)
    
    def get_customers_by_country(self):
        """Group customers by country and return as output model"""
        return CustomersByCountryOutputModel(self.customers)