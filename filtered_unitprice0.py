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