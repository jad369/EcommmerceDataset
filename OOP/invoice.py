class Invoice:

    def __init__(self, invoice_no, invoice_date, customer_id, country):
        self.invoice_no = invoice_no
        self.invoice_date = invoice_date
        self.customer_id = customer_id
        self.country = country
        self.items = []
        self.total = 0

    def add_item(self, product_name, quantity, unit_price):
        """Add an item to the invoice"""
        item = {
            "product": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": quantity * unit_price,
        }
        self.items.append(item)
        self.total += item["subtotal"]

    def get_invoice_total(self):
        """Calculate the total amount of the invoice"""
        return self.total

    def get_item_count(self):
        """Return the number of items in the invoice"""
        return len(self.items)

    def get_items_with_subtotals(self):
        """Return all items with their subtotals"""
        return self.items

    def show(self):
        """Display invoice information"""
        print(f"Invoice: {self.invoice_no}")
        print(f"  Date: {self.invoice_date}")
        print(f"  Items: {len(self.items)}")
        print(f"  Total: ${self.total:.2f}")
