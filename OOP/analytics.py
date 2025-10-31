"""Data analytics module"""

from mappers import CustomerMapper


class DataAnalytics:
    """Class for performing analytics on the data"""
    
    def __init__(self, processor):
        self.processor = processor
    
    def print_business_summary(self):
        print("\n" + "=" * 70)
        print("BUSINESS SUMMARY")
        print("=" * 70)
        
        total_revenue = self.processor.get_total_revenue()
        
        if len(self.processor.invoices) > 0:
            avg_order = total_revenue / len(self.processor.invoices)
        else:
            avg_order = 0
        
        print(f"💰 Total Revenue: ${total_revenue:,.2f}")
        print(f"📦 Total Products: {len(self.processor.products)}")
        print(f"📄 Total Invoices: {len(self.processor.invoices)}")
        print(f"👥 Total Customers: {len(self.processor.customers)}")
        print(f"📊 Average Order Value: ${avg_order:.2f}")
    
    def print_top_customers(self, limit=10):
        print("\n" + "=" * 70)
        print(f"TOP {limit} CUSTOMERS BY SPENDING")
        print("=" * 70)
        
        top_customers = self.processor.get_top_customers(limit)
        
        for i, customer in enumerate(top_customers, 1):
            print(f"{i:2d}. Customer {customer.customer_id} ({customer.country}): ${customer.total_spent:,.2f}")
    
    def print_country_analysis(self):
        print("\n" + "=" * 70)
        print("CUSTOMERS BY COUNTRY")
        print("=" * 70)
        
        by_country = self.processor.get_customers_by_country()
        country_dict = by_country.to_dict()
        
        print(f"Total Countries: {country_dict['total_countries']}")
        
        country_spending = {}
        for country, customers in country_dict['customers_by_country'].items():
            total = 0
            for customer in customers:
                total += customer['total_spent']
            
            country_spending[country] = {
                'count': len(customers),
                'total_spent': total
            }
        
        def get_country_total(country_item):
            country_name = country_item[0]
            data = country_item[1]
            return data['total_spent']
        
        country_items = list(country_spending.items())
        sorted_countries = sorted(country_items, key=get_country_total, reverse=True)
        
        print("\nTop 10 Countries by Revenue:")
        for i in range(min(10, len(sorted_countries))):
            country = sorted_countries[i][0]
            data = sorted_countries[i][1]
            print(f"{i+1:2d}. {country:20s}: {data['count']:4d} customers, ${data['total_spent']:,.2f}")
    
    def print_high_value_invoices(self, threshold=1000, limit=10):
        print("\n" + "=" * 70)
        print(f"HIGH VALUE INVOICES (Over ${threshold:,.2f})")
        print("=" * 70)
        
        high_value = self.processor.get_high_value_invoices(threshold)
        
        print(f"Found {len(high_value)} invoices over ${threshold:,.2f}\n")
        
        max_to_show = min(limit, len(high_value))
        for i in range(max_to_show):
            invoice = high_value[i]
            print(f"{i+1:2d}. Invoice {invoice.invoice_no}: ${invoice.total:,.2f} ({invoice.get_item_count()} items)")
    
    def search_and_display_products(self, search_term, limit=20):
        print("\n" + "=" * 70)
        print(f"SEARCH RESULTS FOR: '{search_term}'")
        print("=" * 70)
        
        results = self.processor.search_products(search_term)
        
        if results:
            print(f"Found {len(results)} products:\n")
            
            max_to_show = min(limit, len(results))
            for i in range(max_to_show):
                product = results[i]
                print(f"{i+1:2d}. {product.stock_code}: {product.description} - ${product.unit_price:.2f}")
            
            if len(results) > limit:
                print(f"\n... and {len(results) - limit} more results")
        else:
            print("No products found")
    
    def print_sample_data(self):
        print("\n" + "=" * 70)
        print("SAMPLE DATA")
        print("=" * 70)
        
        if self.processor.products:
            print("\n📦 Sample Product:")
            products_list = list(self.processor.products.values())
            first_product = products_list[0]
            first_product.show()
        
        if self.processor.customers:
            print("\n👤 Sample Customer:")
            customers_list = list(self.processor.customers.values())
            first_customer = customers_list[0]
            first_customer.show()
        
        if self.processor.invoices:
            print("\n📄 Sample Invoice:")
            invoices_list = list(self.processor.invoices.values())
            first_invoice = invoices_list[0]
            first_invoice.show()