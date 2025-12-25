class Customer:

    def __init__(self, customer_id, country):
        self.customer_id = customer_id
        self.country = country
        self.total_spent = 0
        self.purchase_count = 0

    def add_purchase(self, amount):
        """Record a purchase by this customer"""
        self.total_spent += amount
        self.purchase_count += 1

    def show(self):
        """Display customer information"""
        print(f"Customer: {self.customer_id}")
        print(f"  Country: {self.country}")
        print(f"  Total Spent: ${self.total_spent:.2f}")
        print(f"  Purchases: {self.purchase_count}")
