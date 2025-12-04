import csv
from collections import defaultdict
from io import StringIO


class ReportsGenerator:
    """Generates specific CSV report files from processed data"""
    
    def __init__(self, processor):
        """
        Initialize the reports generator.
        
        Args:
            processor: CSVDataProcessor instance with loaded data
        """
        self.processor = processor
    
    def generate_monthly_sales_2010(self, output_file='monthly_sales_2010.csv'):
        """
        Generate monthly sales report for 2010.
        Output: month, total_quantity, revenue
        
        Args:
            output_file: Path to save the report
        """
        monthly_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})
        
        # Process all invoices
        for invoice in self.processor.invoices.values():
            # Check if invoice is from 2010
            if '2010' in invoice.invoice_date:
                # Extract month from date (assuming format like "1/5/2010 8:00")
                date_parts = invoice.invoice_date.split('/')
                month = int(date_parts[0])  # Month is first part
                
                # Sum quantities and revenue
                for item in invoice.items:
                    monthly_data[month]['quantity'] += item['quantity']
                    monthly_data[month]['revenue'] += item['subtotal']
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['month', 'total_quantity', 'revenue'])
            
            # Sort by month
            for month in sorted(monthly_data.keys()):
                data = monthly_data[month]
                writer.writerow([
                    month,
                    data['quantity'],
                    round(data['revenue'], 2)
                ])
        
        print(f"Generated: {output_file}")
        return True
    
    def generate_monthly_sales_2011(self, output_file='monthly_sales_2011.csv'):
        """
        Generate monthly sales report for 2011.
        Output: month, total_quantity, revenue
        
        Args:
            output_file: Path to save the report
        """
        monthly_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})
        
        # Process all invoices
        for invoice in self.processor.invoices.values():
            # Check if invoice is from 2011
            if '2011' in invoice.invoice_date:
                # Extract month from date
                date_parts = invoice.invoice_date.split('/')
                month = int(date_parts[0])
                
                # Sum quantities and revenue
                for item in invoice.items:
                    monthly_data[month]['quantity'] += item['quantity']
                    monthly_data[month]['revenue'] += item['subtotal']
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['month', 'total_quantity', 'revenue'])
            
            # Sort by month
            for month in sorted(monthly_data.keys()):
                data = monthly_data[month]
                writer.writerow([
                    month,
                    data['quantity'],
                    round(data['revenue'], 2)
                ])
        
        print(f"Generated: {output_file}")
        return True
    
    def generate_stock_by_year(self, output_file='stock_code_by_year.csv'):
        """
        Generate stock code and description by year.
        Output: stock_code, description, year
        
        Args:
            output_file: Path to save the report
        """
        # Track stock codes by year
        stock_by_year = {}  # (stock_code, year) -> description
        
        # Process all invoices
        for invoice in self.processor.invoices.values():
            # Extract year from date
            date_parts = invoice.invoice_date.split('/')
            year = date_parts[2].split()[0]  # Get year part (e.g., "2010" from "2010 8:00")
            
            # Process each item in invoice
            for item in invoice.items:
                product_desc = item['product']
                
                # Find the stock code for this product
                for stock_code, product in self.processor.products.items():
                    if product.description == product_desc:
                        key = (stock_code, year)
                        if key not in stock_by_year:
                            stock_by_year[key] = product_desc
                        break
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['stock_code', 'description', 'year'])
            
            # Sort by year, then stock code
            for (stock_code, year), description in sorted(stock_by_year.items(), key=lambda x: (x[0][1], x[0][0])):
                writer.writerow([stock_code, description, year])
        
        print(f" Generated: {output_file}")
        return True
    
    def generate_country_sales_2010(self, output_file='country_sales_2010.csv'):
        """
        Generate country sales report for 2010.
        Output: country, total_quantity, revenue
        
        Args:
            output_file: Path to save the report
        """
        country_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})
        
        # Process all invoices
        for invoice in self.processor.invoices.values():
            # Check if invoice is from 2010
            if '2010' in invoice.invoice_date:
                country = invoice.country
                
                # Sum quantities and revenue for this country
                for item in invoice.items:
                    country_data[country]['quantity'] += item['quantity']
                    country_data[country]['revenue'] += item['subtotal']
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['country', 'total_quantity', 'revenue'])
            
            # Sort by country name
            for country in sorted(country_data.keys()):
                data = country_data[country]
                writer.writerow([
                    country,
                    data['quantity'],
                    round(data['revenue'], 2)
                ])
        
        print(f"Generated: {output_file}")
        return True
    
    def generate_country_sales_2011(self, output_file='country_sales_2011.csv'):
        """
        Generate country sales report for 2011.
        Output: country, total_quantity, revenue
        
        Args:
            output_file: Path to save the report
        """
        country_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})
        
        # Process all invoices
        for invoice in self.processor.invoices.values():
            # Check if invoice is from 2011
            if '2011' in invoice.invoice_date:
                country = invoice.country
                
                # Sum quantities and revenue for this country
                for item in invoice.items:
                    country_data[country]['quantity'] += item['quantity']
                    country_data[country]['revenue'] += item['subtotal']
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['country', 'total_quantity', 'revenue'])
            
            # Sort by country name
            for country in sorted(country_data.keys()):
                data = country_data[country]
                writer.writerow([
                    country,
                    data['quantity'],
                    round(data['revenue'], 2)
                ])
        
        print(f"Generated: {output_file}")
        return True
    
    def generate_all_reports(self):
        """
        Generate all report files at once.
        """
        print("\n" + "=" * 70)
        print("GENERATING REPORT FILES")
        print("=" * 70 + "\n")
        
        self.generate_monthly_sales_2010()
        self.generate_monthly_sales_2011()
        self.generate_stock_by_year()
        self.generate_country_sales_2010()
        self.generate_country_sales_2011()
        
        print("\n" + "=" * 70)
        print("ALL REPORTS GENERATED SUCCESSFULLY!")
        print("=" * 70)
        print("\n Output files created:")
        print("   1. final_dataset.csv (cleaned data)")
        print("   2. monthly_sales_2010.csv")
        print("   3. monthly_sales_2011.csv")
        print("   4. stock_code_by_year.csv")
        print("   5. country_sales_2010.csv")
        print("   6. country_sales_2011.csv")
        print("=" * 70 + "\n")
