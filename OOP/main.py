import csv
from product import Product
from invoice import Invoice
from customer import Customer


# ========== DATA PROCESSOR CLASS ==========

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
            
            print(f"✅ Successfully processed {row_count} rows")
            print(f"   - Products: {len(self.products)}")
            print(f"   - Invoices: {len(self.invoices)}")
            print(f"   - Customers: {len(self.customers)}")
            
        except FileNotFoundError:
            print(f"❌ ERROR: File '{self.csv_filename}' not found")
            print("   Make sure the file is in the same folder as this script")
        except IndexError as e:
            print(f"❌ ERROR: CSV file has wrong structure - {e}")
            print("   Check that your CSV has the correct columns")
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    def _process_row(self, row):
        """Process a single CSV row (private method)"""
        invoice_no = row[0]
        stock_code = row[1]
        description = row[2]
        quantity = int(row[3])
        price = float(row[5])
        customer_id = row[6]
        country = row[7]
        invoice_date = row[4]
        
        # Create or get product
        if stock_code not in self.products:
            self.products[stock_code] = Product(stock_code, description, price)
        
        # Create or get invoice and add item
        if invoice_no not in self.invoices:
            self.invoices[invoice_no] = Invoice(invoice_no, invoice_date, None, None)
        self.invoices[invoice_no].add_item(description, quantity, price)
        
        # Create or get customer and add purchase
        if customer_id not in self.customers:
            self.customers[customer_id] = Customer(customer_id, country)
        self.customers[customer_id].add_purchase(quantity * price)
    
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
    
    def get_customers_by_country(self):
        """Group customers by country and return as output model"""
        return CustomersByCountryOutputModel(self.customers)


# ========== DATA ANALYTICS CLASS ==========

class DataAnalytics:
    """Class for performing analytics on the data"""
    
    def __init__(self, processor):
        self.processor = processor
    
    def print_business_summary(self):
        print("\n" + "=" * 70)
        print("BUSINESS SUMMARY")
        print("=" * 70)
        
        total_revenue = self.processor.get_total_revenue()
        
        if len(self.processor.invoices) > 0:
            avg_order = total_revenue / len(self.processor.invoices)
        else:
            avg_order = 0
        
        print(f"💰 Total Revenue: ${total_revenue:,.2f}")
        print(f"📦 Total Products: {len(self.processor.products)}")
        print(f"📄 Total Invoices: {len(self.processor.invoices)}")
        print(f"👥 Total Customers: {len(self.processor.customers)}")
        print(f"📊 Average Order Value: ${avg_order:.2f}")
    
    def print_top_customers(self, limit=10):
        print("\n" + "=" * 70)
        print(f"TOP {limit} CUSTOMERS BY SPENDING")
        print("=" * 70)
        
        top_customers = self.processor.get_top_customers(limit)
        
        for i, customer in enumerate(top_customers, 1):
            print(f"{i:2d}. Customer {customer.customer_id} ({customer.country}): ${customer.total_spent:,.2f}")
    
    def print_country_analysis(self):
        print("\n" + "=" * 70)
        print("CUSTOMERS BY COUNTRY")
        print("=" * 70)
        
        by_country = self.processor.get_customers_by_country()
        country_dict = by_country.to_dict()
        
        print(f"Total Countries: {country_dict['total_countries']}")
        
        country_spending = {}
        for country, customers in country_dict['customers_by_country'].items():
            total = 0
            for customer in customers:
                total += customer['total_spent']
            
            country_spending[country] = {
                'count': len(customers),
                'total_spent': total
            }
        
        def get_country_total(country_item):
            country_name = country_item[0]
            data = country_item[1]
            return data['total_spent']
        
        country_items = list(country_spending.items())
        sorted_countries = sorted(country_items, key=get_country_total, reverse=True)
        
        print("\nTop 10 Countries by Revenue:")
        for i in range(min(10, len(sorted_countries))):
            country = sorted_countries[i][0]
            data = sorted_countries[i][1]
            print(f"{i+1:2d}. {country:20s}: {data['count']:4d} customers, ${data['total_spent']:,.2f}")
    
    def print_high_value_invoices(self, threshold=1000, limit=10):
        print("\n" + "=" * 70)
        print(f"HIGH VALUE INVOICES (Over ${threshold:,.2f})")
        print("=" * 70)
        
        high_value = self.processor.get_high_value_invoices(threshold)
        
        print(f"Found {len(high_value)} invoices over ${threshold:,.2f}\n")
        
        max_to_show = min(limit, len(high_value))
        for i in range(max_to_show):
            invoice = high_value[i]
            print(f"{i+1:2d}. Invoice {invoice.invoice_no}: ${invoice.total:,.2f} ({invoice.get_item_count()} items)")
    
    def search_and_display_products(self, search_term, limit=20):
        print("\n" + "=" * 70)
        print(f"SEARCH RESULTS FOR: '{search_term}'")
        print("=" * 70)
        
        results = self.processor.search_products(search_term)
        
        if results:
            print(f"Found {len(results)} products:\n")
            
            max_to_show = min(limit, len(results))
            for i in range(max_to_show):
                product = results[i]
                print(f"{i+1:2d}. {product.stock_code}: {product.description} - ${product.unit_price:.2f}")
            
            if len(results) > limit:
                print(f"\n... and {len(results) - limit} more results")
        else:
            print("No products found")
    
    def print_sample_data(self):
        print("\n" + "=" * 70)
        print("SAMPLE DATA")
        print("=" * 70)
        
        if self.processor.products:
            print("\n📦 Sample Product:")
            products_list = list(self.processor.products.values())
            first_product = products_list[0]
            first_product.show()
        
        if self.processor.customers:
            print("\n👤 Sample Customer:")
            customers_list = list(self.processor.customers.values())
            first_customer = customers_list[0]
            first_customer.show()
        
        if self.processor.invoices:
            print("\n📄 Sample Invoice:")
            invoices_list = list(self.processor.invoices.values())
            first_invoice = invoices_list[0]
            first_invoice.show()


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


# ========== MAPPER CLASSES ==========

class ProductMapper:
    """Maps between CSV data and Product objects"""
    
    @staticmethod
    def from_csv_row(row):
        """Create a Product from a CSV row"""
        stock_code = row[1]
        description = row[2]
        price = float(row[5])
        return Product(stock_code, description, price)
    
    @staticmethod
    def to_output_model(product):
        """Convert Product to ProductOutputModel"""
        return ProductOutputModel(product)
    
    @staticmethod
    def to_dict(product):
        """Convert Product to dictionary"""
        output_model = ProductMapper.to_output_model(product)
        return output_model.to_dict()
    
    @staticmethod
    def collection_to_catalog(products_dict):
        """Convert all Products to catalog output model"""
        return ProductCatalogOutputModel(products_dict)


class InvoiceMapper:
    """Maps between CSV data and Invoice objects"""
    
    @staticmethod
    def from_csv_row(row):
        """Create an Invoice from a CSV row"""
        invoice_no = row[0]
        invoice_date = row[4]
        return Invoice(invoice_no, invoice_date, None, None)
    
    @staticmethod
    def add_item_from_csv_row(invoice, row):
        """Add an item to Invoice from CSV row"""
        description = row[2]
        quantity = int(row[3])
        price = float(row[5])
        invoice.add_item(description, quantity, price)
    
    @staticmethod
    def to_output_model(invoice):
        """Convert Invoice to InvoiceOutputModel"""
        return InvoiceOutputModel(invoice)
    
    @staticmethod
    def to_dict(invoice):
        """Convert Invoice to dictionary"""
        output_model = InvoiceMapper.to_output_model(invoice)
        return output_model.to_dict()
    
    @staticmethod
    def collection_to_summary(invoices_dict):
        """Convert all Invoices to summary output model"""
        return InvoiceSummaryOutputModel(invoices_dict)


class CustomerMapper:
    """Maps between CSV data and Customer objects"""
    
    @staticmethod
    def from_csv_row(row):
        """Create a Customer from a CSV row"""
        customer_id = row[6]
        country = row[7]
        return Customer(customer_id, country)
    
    @staticmethod
    def add_purchase_from_csv_row(customer, row):
        """Add a purchase to Customer from CSV row"""
        quantity = int(row[3])
        price = float(row[5])
        sale_amount = quantity * price
        customer.add_purchase(sale_amount)
    
    @staticmethod
    def to_output_model(customer):
        """Convert Customer to CustomerOutputModel"""
        return CustomerOutputModel(customer)
    
    @staticmethod
    def to_dict(customer):
        """Convert Customer to dictionary"""
        output_model = CustomerMapper.to_output_model(customer)
        return output_model.to_dict()
    
    @staticmethod
    def collection_to_summary(customers_dict):
        """Convert all Customers to summary output model"""
        return CustomerSummaryOutputModel(customers_dict)
    
    @staticmethod
    def group_by_country(customers_dict):
        """Group customers by country"""
        return CustomersByCountryOutputModel(customers_dict)

#merge scipt

import csv

file1 = '09_10_dataset.csv'
file2 = '10_11_dataset.csv'
output_file = 'merged_dataset.csv'

#Open output file in write mode
with open(output_file, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)

    # Process first file
    with open(file1, 'r') as f1:
        csv_reader = csv.reader(f1)
        for row in csv_reader:
            csv_writer.writerow(row) 

    #Process the second file
    with open(file2, 'r') as f2:
        csv_reader = csv.reader(f2)
        next(csv_reader)
        for row in csv_reader: 
            csv_writer.writerow(row) 

print(f"Files merged sucessfully into '{output_file}'!")

#deduplicate invoice numbers

import csv

input_file = 'merged_dataset.csv'
output_file = 'deduplicated_dataset.csv'

seen_invoice_numbers = set()

rows_to_keep = []

try:
    with open(input_file) as infile:
        csv_reader = csv.reader(infile)

        #Read the header and add it to list
        header = next(csv_reader)
        rows_to_keep.append(header)

        #Loop through the rest of the rows
        for row in csv_reader:
            invoice_number = row [0]

            if invoice_number not in seen_invoice_numbers:
                rows_to_keep.append(row)
                seen_invoice_numbers.add(invoice_number)

    with open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerows(rows_to_keep)

    print(f"Succesfully removed duplicates and saved file as '{output_file}'.") 

except FileNotFoundError:
    print(f"Error: The file {input_file}' was not found. Please make sure it's in the same folder as the script.")   

#Filter out Invoice that starts with C

import csv

input_file = 'deduplicated_dataset.csv'
output_file = 'filtered_dataset.csv'

rows_to_keep = []

try:
    with open(input_file, 'r', newline='') as infile:
        csv_reader = csv.reader(infile)

        #Read the header and add it to the list
        header = next(csv_reader)
        rows_to_keep.append(header)

        #Loop through the rest of the rows in the file
        for row in csv_reader:
            invoice_number = row[0]
            
            if not invoice_number.strip().startswith('C'):
                rows_to_keep.append(row)

    with open(output_file, 'w', newline = '') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerows(rows_to_keep)
        
    print(f"Succesfully filtered cancelled invoices and saved the file as '{output_file}'.")

except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found. Please make sure it is in the same folder the script is in.")

#Filter out year 2009

import csv

#File names
input_file = 'filtered_dataset.csv'
output_file = 'no_2009_dataset.csv'

#List to store rows to keep
rows_to_keep = []

try:
    #Open and read the csv file
    with open(input_file, 'r', newline='') as infile:
        csv_reader = csv.reader(infile)

        #Read the header row first
        header = next(csv_reader)
        rows_to_keep.append(header) 

        #Go through each row of the file
        for row in csv_reader:
            #Get the invoice date
            invoice_date = row[4]

            #Check if the date cotains 2009
            if "2009" not in invoice_date:
                #If it doesn't keep the row
                rows_to_keep.append(row)
    #Write filtered data to new file
    with open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerows(rows_to_keep)
    print(f"Succesfully removed all 2009 rows!")
    print(f"Original data saved as {output_file}'")

except FileNotFoundError:
    print(f"Error: could not find the file {input_file}'")
    print("Make sure the file is in the same folder as the script")
          
except Exception as e:
    print(f"An error occured: {e}")

#Filter out unit price 0

import csv

input_file = 'no_2009_dataset.csv'
output_file = 'clean_dataset.csv'

rows_to_keep =[]

with open(input_file, 'r', newline ='') as infile:
    csv_reader = csv.reader(infile)

    header = next(csv_reader)
    rows_to_keep.append(header)

    for row in csv_reader:
        unit_price = row[5]

        if unit_price != "0":
            rows_to_keep.append(row)

with open(output_file, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerows(rows_to_keep)

print("Zero price rows removed!")

# FIlter out TEST001 Stock Code

import csv

input_file = 'clean_dataset.csv'
output_file = 'final_dataset.csv'

rows_to_keep = []

with open(input_file, 'r', newline='') as infile:
    csv_reader = csv.reader(infile)

    header = next(csv_reader)
    rows_to_keep.append(header)

    for row in csv_reader:
        stock_code = row[1]

        if stock_code != "TEST001":
            rows_to_keep.append(row)

with open(output_file, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerows(rows_to_keep)

print("Test stock code rows removed!")



# ========== EXAMPLE USAGE ==========

if __name__ == "__main__":
    # Example: Load data and run analytics
    print("Loading data from CSV...")
    processor = CSVDataProcessor('final_dataset.csv')
    processor.load_data()
    
    # Create analytics instance
    analytics = DataAnalytics(processor)
    
    # Run various analytics
    analytics.print_business_summary()
    analytics.print_top_customers(limit=10)
    analytics.print_country_analysis()

