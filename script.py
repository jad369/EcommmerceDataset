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
