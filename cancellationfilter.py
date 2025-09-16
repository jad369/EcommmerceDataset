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