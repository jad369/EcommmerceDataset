#Domain Models

class Product:

    def __init__(self, stock_code, description, unit_price):
        self.stock_code = stock_code
        self.description = description
        self.unit_price = unit_price

    def show(self):
        print(f"{self.stock_code}: {self.description} (${self.unit_price})")

class Invoice:
    def __init__(self, invoice_no, invoice_date):
        self.invoice_no = invoice_no
        self.invoice_date = invoice_date
        self.main_product = None
        self.main_quantity = None
        self.total = 0
        self.items = []

    def add_item(self, product, quantity, price):
        subtotal = quantity * price

        self.items.append({
            'product': product,
            'quantity': quantity,
            'unit_price': price,
            'subtotal': subtotal
        })

        self.total += subtotal

        if self.main_product is None:
            self.main_product = product
            self.main_quantity = quantity

    def get_invoice_total(self):
        return self.items
    
    def get_main_products(self):
        return self.main_product
    
    def get_main_quanitity(self):
        return self.main_quantity
    
    def get_item_count(self):
        return len(self.items)
    
    def get_total_quantity(self):
        total = 0
        for items in self.items:
            total += items['quantity']
        return total
    
    def show(self):
        print(f"Invoice {self.invoice_no} (Date: {self.invoice_date})")
        print(f"Total: ${self.total:.2f}")

        if self.main_product:
            print(f"Main Product: {self.main_product} (Qty: {self.main_quantity})")

        print(f"Items on Invoice: {self.get_item_count()}")
        print(f"Total Quantity: {self.get_total_quantity()}")
        print("\nAll Items:")
        for item in self.items:
            print(f"  - {item['product']}: {item['quantity']} x ${item['unit_price']:.2f} = ${item['subtotal']:.2f}")


class Customer:
    def __init__(self, customer_id, country):
        self.customer_id = customer_id
        self.country = country
        self.total_spent = 0

    def add_purchase(self, amount):
        self.total_spent += amount

    def show(self):
        print(f"Customer {self.customer_id} from {self.country} spent: ${self.total_spent:.2f}")