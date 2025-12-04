from data_cleaner import DataCleaner
from processors import CSVDataProcessor
from analytics import DataAnalytics
from reports import ReportsGenerator




# ========== MAIN EXECUTION ==========

if __name__ == "__main__":
    # ===== STEP 1: Run data cleaning pipeline =====
    print("\n" + "="*70)
    print("STEP 1: DATA CLEANING")
    print("="*70)
    print("\nCleaning data from original files:")
    print("  - Input File 1: 09_10_dataset.csv")
    print("  - Input File 2: 10_11_dataset.csv")
    print("  - Output File: final_dataset.csv\n")
    
    # Create DataCleaner instance and run full pipeline
    cleaner = DataCleaner()
    cleaner.run_full_pipeline(
        file1='09_10_dataset.csv',
        file2='10_11_dataset.csv',
        output_file='final_dataset.csv'
    )
    
    # ===== STEP 2: Run analytics on cleaned data =====
    print("\n" + "="*70)
    print("STEP 2: DATA PROCESSING")
    print("="*70)
    print("\nLoading cleaned data from: final_dataset.csv\n")
    
    processor = CSVDataProcessor('final_dataset.csv')
    processor.load_data()
    
    # Create analytics instance
    analytics = DataAnalytics(processor)
    
    # Run various analytics
    analytics.print_business_summary()
    analytics.print_top_customers(limit=10)
    analytics.print_country_analysis()
    
    # ===== STEP 3: Generate specific report files =====
    reports = ReportsGenerator(processor)
    reports.generate_all_reports()
    
    print("\n" + "="*70)
    print("COMPLETE! All steps finished successfully.")
    print("="*70)