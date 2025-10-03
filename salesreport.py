#Calculate monthly sales for 2010 and 2011

import csv

input_file = 'final_dataset.csv'
output_file = 'monthly_sales.csv'

#Dictionary to store sales for each month
monthly_data = {}

with open(input_file, 'r', newline='') as infile:
    csv_reader = csv.reader(infile)

    header = next(csv_reader)

    for row in csv_reader:
        invoice_date = row[4]
        quantity = row[3]
        unit_price = row[5]

        #Extract month and year from date
        date_parts = invoice_date.split('/')
        month = date_parts[0].zfill(2)
        year = date_parts[2].split()[0]

        #Create year month key
        year_month = f"{year}-{month}"

        #Calculate revenue from this row
        revenue = float(quantity) * float(unit_price)

        #Add to monthly totals
        if year_month in monthly_data:
            monthly_data[year_month]['quantity'] += int(quantity)
            monthly_data[year_month]['revenue'] += revenue
        else:
            monthly_data[year_month] = {
                'quantity':int(quantity),
                'revenue': revenue
            }

#Write results to CSV

with open(output_file, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)

    #Write header
    csv_writer.writerow(['Year-Month', 'Total Quantity', 'Revenue'])

    #Write each month's data sorted by year-month
    for year_month in sorted(monthly_data.keys()):
        quantity = monthly_data[year_month]['quantity']
        revenue = monthly_data[year_month]['revenue']
        csv_writer.writerow([year_month, quantity, f'{revenue:.2f}'])

print("Monthly sales report created!")
print("\nSummary:")
for year_month in sorted(monthly_data.keys()):
    quantity = monthly_data[year_month]['quantity']
    revenue = monthly_data[year_month]['revenue']
    print(f"{year_month}: {quantity} items sold, ${revenue:.2f} revenue")