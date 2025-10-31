from processor import CSVDataProcessor
from analytics import DataAnalytics


# ========== MAIN EXECUTION ==========

if __name__ == "__main__":
    
    print("=" * 70)
    print("E-COMMERCE DATA ANALYSIS SYSTEM")
    print("=" * 70)
    print()
    
    # Create processor and load data
    processor = CSVDataProcessor('final_dataset.csv')
    processor.load_data()
    
    # Check if data loaded successfully
    if len(processor.products) == 0:
        print("\n No data loaded. Please check your CSV file and try again.")
    else:
        #Create analytics object
        analytics = DataAnalytics(processor)
        
        #Display various analytics
        analytics.print_business_summary()
        analytics.print_top_customers(10)
        analytics.print_country_analysis()
        analytics.print_high_value_invoices(1000, 10)
        analytics.search_and_display_products("HEART", 15)
        analytics.print_sample_data()
        
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)
        print()
        print("You can now use the 'processor' object to access your data:")
        print("   - processor.get_customer('customer_id')")
        print("   - processor.get_product('stock_code')")
        print("   - processor.get_invoice('invoice_no')")
        print()