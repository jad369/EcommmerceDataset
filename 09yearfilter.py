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