# Get unique stock codes and descriptions by year

import csv

input_file = 'final_dataset.csv'
output_file = 'stock_by_year.csv'


# Dictionary to store products for each year
products_by_year = {}

with open(input_file, 'r', newline='') as infile:
    csv_reader = csv.reader(infile)
    
    header = next(csv_reader)
    
    for row in csv_reader:
        stock_code = row[1]
        description = row[2]
        invoice_date = row[4]
        
        # Extract year from date
        year = invoice_date.split('/')[2].split()[0]
        
        # Create a unique key for each product (stockcode-description)
        product_key = f"{stock_code}-{description}"
        
        # Add year to our dictionary if not already there
        if year not in products_by_year:
            products_by_year[year] = {}
        
        # Add product to this year (only if we haven't seen it before)
        if product_key not in products_by_year[year]:
            products_by_year[year][product_key] = {
                'stock_code': stock_code,
                'description': description
            }

# Reorganize data to sort by stock code first
all_products = []

for year in products_by_year.keys():
    for product_key in products_by_year[year].keys():
        stock_code = products_by_year[year][product_key]['stock_code']
        description = products_by_year[year][product_key]['description']
        all_products.append([stock_code, year, description])

# Sort by stock code, then by year
all_products.sort()

# Write results to CSV
with open(output_file, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    
    # Write header
    csv_writer.writerow(['StockCode', 'Year', 'Description'])
    
    # Write all products
    for product in all_products:
        csv_writer.writerow(product)

print("Products per year report created!")
print("\nSummary:")
for year in sorted(products_by_year.keys()):
    num_products = len(products_by_year[year])
    print(f"Year {year}: {num_products} unique products")