class Product:
    
    def __init__(self, stock_code, description, unit_price): 
        self.stock_code = stock_code
        self.description = description
        self.unit_price = unit_price
    
    def show(self):
        """Display product information"""
        print(f"Product: {self.stock_code}")
        print(f"  Description: {self.description}")
        print(f"  Price: ${self.unit_price:.2f}")