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

