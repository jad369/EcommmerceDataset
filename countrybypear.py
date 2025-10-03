# Calculate sales by country for each year

import csv

input_file = 'final_dataset.csv'
output_file = 'country_sales_by_year.csv'

# Dictionary to store sales for each country-year
country_year_data = {}

with open(input_file, 'r', newline='') as infile:
    csv_reader = csv.reader(infile)
    
    header = next(csv_reader)
    
    for row in csv_reader:
        country = row[7]
        invoice_date = row[4]
        quantity = row[3]
        unit_price = row[5]
        
        # Extract year from date 
        year = invoice_date.split('/')[2].split()[0]
        
        # Calculate revenue for this row
        revenue = float(quantity) * float(unit_price)
        
        # Create country-year key
        country_year = f"{country}-{year}"
        
        # Add to totals
        if country_year in country_year_data:
            country_year_data[country_year]['quantity'] += int(quantity)
            country_year_data[country_year]['revenue'] += revenue
        else:
            country_year_data[country_year] = {
                'country': country,
                'year': year,
                'quantity': int(quantity),
                'revenue': revenue
            }

# Organize data for sorting by country first
all_sales = []

for country_year in country_year_data.keys():
    country = country_year_data[country_year]['country']
    year = country_year_data[country_year]['year']
    quantity = country_year_data[country_year]['quantity']
    revenue = country_year_data[country_year]['revenue']
    all_sales.append([country, year, quantity, revenue])

# Sort by country, then by year
all_sales.sort()

# Write results to CSV
with open(output_file, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    
    # Write header
    csv_writer.writerow(['Country', 'Year', 'Total Quantity', 'Revenue'])
    
    # Write all sales data
    for sale in all_sales:
        country = sale[0]
        year = sale[1]
        quantity = sale[2]
        revenue = sale[3]
        csv_writer.writerow([country, year, quantity, f'{revenue:.2f}'])

print("Country sales by year report created!")
print("\nSummary:")
for sale in all_sales:
    country = sale[0]
    year = sale[1]
    quantity = sale[2]
    revenue = sale[3]
    print(f"{country} - {year}: {quantity} items sold, ${revenue:.2f} revenue")