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
