"""
Data Cleaner
Object-oriented data cleaning pipeline using StringIO for efficient in-memory operations.

Expected Input Files:
  - 09_10_dataset.csv (December 2009 - November 2010 data)
  - 10_11_dataset.csv (December 2010 - November 2011 data)

Output File:
  - final_dataset.csv (Merged and cleaned data)

Cleaning Steps:
  1. Merge the two CSV files
  2. Filter out cancelled invoices (starting with 'C')
  3. Remove year 2009 data
  4. Remove rows with zero prices
  5. Remove test stock codes (TEST001)
"""

import csv
from io import StringIO


class DataCleaner:
    """Handles data cleaning operations on CSV files"""
    
    def __init__(self):
        """Initialize the DataCleaner"""
        self.current_data = None
        self.steps_completed = []
    
    def load_file(self, filename):
        """
        Load a CSV file into memory.
        
        Args:
            filename: Path to the CSV file to load
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.current_data = file.read()
            print(f"✅ Loaded '{filename}' into memory")
            return True
        except FileNotFoundError:
            print(f"❌ Error: File '{filename}' not found")
            return False
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def save_to_file(self, filename):
        """
        Save current data to a CSV file.
        
        Args:
            filename: Path where to save the file
        """
        try:
            # Remove any \r characters to prevent double line breaks
            clean_data = self.current_data.replace('\r', '')
            
            with open(filename, 'w', encoding='utf-8', newline='') as file:
                file.write(clean_data)
            print(f"✅ Saved data to '{filename}'")
            return True
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return False
    
    def merge_files(self, file1, file2):
        """
        Merge two CSV files into current data.
        
        Args:
            file1: First CSV file path
            file2: Second CSV file path
        """
        try:
            # Read first file
            with open(file1, 'r', encoding='utf-8') as f1:
                data1 = f1.read()
            
            # Read second file
            with open(file2, 'r', encoding='utf-8') as f2:
                lines = f2.readlines()
                # Skip the header (first line) from second file
                data2 = ''.join(lines[1:])
            
            # Merge the data
            self.current_data = data1 + data2
            self.steps_completed.append("merge_files")
            print(f"✅ Merged '{file1}' and '{file2}' successfully")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Error: File not found - {e}")
            return False
        except Exception as e:
            print(f"❌ Error merging files: {e}")
            return False
    
    
    def filter_cancelled_invoices(self):
        """
        Remove invoices starting with 'C' (cancelled orders).
        """
        if self.current_data is None:
            print("❌ No data loaded. Load a file first.")
            return False
        
        # Create StringIO objects
        input_stream = StringIO(self.current_data)
        output_stream = StringIO()
        
        csv_reader = csv.reader(input_stream)
        csv_writer = csv.writer(output_stream)
        
        # Read header
        header = next(csv_reader)
        csv_writer.writerow(header)
        
        # Process rows
        rows_kept = 0
        rows_removed = 0
        for row in csv_reader:
            invoice_number = row[0].strip()
            
            if not invoice_number.startswith('C'):
                csv_writer.writerow(row)
                rows_kept += 1
            else:
                rows_removed += 1
        
        # Update current data
        self.current_data = output_stream.getvalue()
        self.steps_completed.append("filter_cancelled_invoices")
        
        print(f"✅ Removed {rows_removed} cancelled invoices")
        print(f"   Kept {rows_kept} valid invoices")
        return True
    
    def filter_by_year(self, year_to_exclude):
        """
        Remove rows from a specific year.
        
        Args:
            year_to_exclude: Year to filter out (e.g., "2009")
        """
        if self.current_data is None:
            print("❌ No data loaded. Load a file first.")
            return False
        
        # Create StringIO objects
        input_stream = StringIO(self.current_data)
        output_stream = StringIO()
        
        csv_reader = csv.reader(input_stream)
        csv_writer = csv.writer(output_stream)
        
        # Read header
        header = next(csv_reader)
        csv_writer.writerow(header)
        
        # Process rows
        rows_kept = 0
        rows_removed = 0
        for row in csv_reader:
            invoice_date = row[4]
            
            if str(year_to_exclude) not in invoice_date:
                csv_writer.writerow(row)
                rows_kept += 1
            else:
                rows_removed += 1
        
        # Update current data
        self.current_data = output_stream.getvalue()
        self.steps_completed.append(f"filter_year_{year_to_exclude}")
        
        print(f"✅ Removed {rows_removed} rows from year {year_to_exclude}")
        print(f"   Kept {rows_kept} rows")
        return True
    
    def filter_zero_prices(self):
        """
        Remove rows with unit price of 0.
        """
        if self.current_data is None:
            print("❌ No data loaded. Load a file first.")
            return False
        
        # Create StringIO objects
        input_stream = StringIO(self.current_data)
        output_stream = StringIO()
        
        csv_reader = csv.reader(input_stream)
        csv_writer = csv.writer(output_stream)
        
        # Read header
        header = next(csv_reader)
        csv_writer.writerow(header)
        
        # Process rows
        rows_kept = 0
        rows_removed = 0
        for row in csv_reader:
            unit_price = row[5]
            
            if unit_price != "0" and unit_price != "0.0":
                csv_writer.writerow(row)
                rows_kept += 1
            else:
                rows_removed += 1
        
        # Update current data
        self.current_data = output_stream.getvalue()
        self.steps_completed.append("filter_zero_prices")
        
        print(f"✅ Removed {rows_removed} rows with zero price")
        print(f"   Kept {rows_kept} rows")
        return True
    
    def filter_by_stock_code(self, stock_code_to_exclude):
        """
        Remove rows with specific stock code.
        
        Args:
            stock_code_to_exclude: Stock code to filter out (e.g., "TEST001")
        """
        if self.current_data is None:
            print("❌ No data loaded. Load a file first.")
            return False
        
        # Create StringIO objects
        input_stream = StringIO(self.current_data)
        output_stream = StringIO()
        
        csv_reader = csv.reader(input_stream)
        csv_writer = csv.writer(output_stream)
        
        # Read header
        header = next(csv_reader)
        csv_writer.writerow(header)
        
        # Process rows
        rows_kept = 0
        rows_removed = 0
        for row in csv_reader:
            stock_code = row[1]
            
            if stock_code != stock_code_to_exclude:
                csv_writer.writerow(row)
                rows_kept += 1
            else:
                rows_removed += 1
        
        # Update current data
        self.current_data = output_stream.getvalue()
        self.steps_completed.append(f"filter_stock_code_{stock_code_to_exclude}")
        
        print(f"✅ Removed {rows_removed} rows with stock code '{stock_code_to_exclude}'")
        print(f"   Kept {rows_kept} rows")
        return True
    
    def get_row_count(self):
        """
        Get the current number of rows (excluding header).
        
        Returns:
            Number of data rows
        """
        if self.current_data is None:
            return 0
        
        input_stream = StringIO(self.current_data)
        csv_reader = csv.reader(input_stream)
        next(csv_reader)  # Skip header
        
        count = sum(1 for row in csv_reader)
        return count
    
    def print_summary(self):
        """Print a summary of cleaning steps completed"""
        print("\n" + "=" * 70)
        print("DATA CLEANING SUMMARY")
        print("=" * 70)
        print(f"Steps completed: {len(self.steps_completed)}")
        for i, step in enumerate(self.steps_completed, 1):
            print(f"  {i}. {step}")
        print(f"\nFinal row count: {self.get_row_count():,} rows")
        print("=" * 70 + "\n")
    
    def run_full_pipeline(self, file1, file2, output_file):
        """
        Run the complete data cleaning pipeline.
        Only saves the final cleaned dataset.
        
        Args:
            file1: First input CSV file
            file2: Second input CSV file
            output_file: Final output file path
        """
        print("\n" + "=" * 70)
        print("STARTING DATA CLEANING PIPELINE")
        print("=" * 70 + "\n")
        
        # Step 1: Merge files
        print("Step 1: Merging datasets...")
        if not self.merge_files(file1, file2):
            return False
        
        # Step 2: Filter cancelled invoices
        print("\nStep 2: Filtering cancelled invoices...")
        if not self.filter_cancelled_invoices():
            return False
        
        # Step 3: Filter year 2009
        print("\nStep 3: Removing 2009 data...")
        if not self.filter_by_year("2009"):
            return False
        
        # Step 4: Filter zero prices
        print("\nStep 4: Removing zero price rows...")
        if not self.filter_zero_prices():
            return False
        
        # Step 5: Filter test stock codes
        print("\nStep 5: Removing test stock codes...")
        if not self.filter_by_stock_code("TEST001"):
            return False
        
        # Save final result only
        print("\nStep 6: Saving final dataset...")
        if not self.save_to_file(output_file):
            return False
        
        # Print summary
        self.print_summary()
        
        print("=" * 70)
        print("DATA CLEANING PIPELINE COMPLETED!")
        print(f"✅ Clean dataset saved as: '{output_file}'")
        print("=" * 70 + "\n")
        
        return True