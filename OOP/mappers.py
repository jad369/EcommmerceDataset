from customer import Customer
from invoice import Invoice
from output_models import (CustomerOutputModel, CustomersByCountryOutputModel,
                           CustomerSummaryOutputModel, InvoiceOutputModel,
                           InvoiceSummaryOutputModel,
                           ProductCatalogOutputModel, ProductOutputModel)
from product import Product


class ProductMapper:
    """Maps between CSV data and Product objects"""

    @staticmethod
    def from_csv_row(row):
        """Create a Product from a CSV row"""
        stock_code = row[1]
        description = row[2]
        price = float(row[5])
        return Product(stock_code, description, price)

    @staticmethod
    def to_output_model(product):
        """Convert Product to ProductOutputModel"""
        return ProductOutputModel(product)

    @staticmethod
    def to_dict(product):
        """Convert Product to dictionary"""
        output_model = ProductMapper.to_output_model(product)
        return output_model.to_dict()

    @staticmethod
    def collection_to_catalog(products_dict):
        """Convert all Products to catalog output model"""
        return ProductCatalogOutputModel(products_dict)


class InvoiceMapper:
    """Maps between CSV data and Invoice objects"""

    @staticmethod
    def from_csv_row(row):
        """Create an Invoice from a CSV row"""
        invoice_no = row[0]
        invoice_date = row[4]
        return Invoice(invoice_no, invoice_date, None, None)

    @staticmethod
    def add_item_from_csv_row(invoice, row):
        """Add an item to Invoice from CSV row"""
        description = row[2]
        quantity = int(row[3])
        price = float(row[5])
        invoice.add_item(description, quantity, price)

    @staticmethod
    def to_output_model(invoice):
        """Convert Invoice to InvoiceOutputModel"""
        return InvoiceOutputModel(invoice)

    @staticmethod
    def to_dict(invoice):
        """Convert Invoice to dictionary"""
        output_model = InvoiceMapper.to_output_model(invoice)
        return output_model.to_dict()

    @staticmethod
    def collection_to_summary(invoices_dict):
        """Convert all Invoices to summary output model"""
        return InvoiceSummaryOutputModel(invoices_dict)


class CustomerMapper:
    """Maps between CSV data and Customer objects"""

    @staticmethod
    def from_csv_row(row):
        """Create a Customer from a CSV row"""
        customer_id = row[6]
        country = row[7]
        return Customer(customer_id, country)

    @staticmethod
    def add_purchase_from_csv_row(customer, row):
        """Add a purchase to Customer from CSV row"""
        quantity = int(row[3])
        price = float(row[5])
        sale_amount = quantity * price
        customer.add_purchase(sale_amount)

    @staticmethod
    def to_output_model(customer):
        """Convert Customer to CustomerOutputModel"""
        return CustomerOutputModel(customer)

    @staticmethod
    def to_dict(customer):
        """Convert Customer to dictionary"""
        output_model = CustomerMapper.to_output_model(customer)
        return output_model.to_dict()

    @staticmethod
    def collection_to_summary(customers_dict):
        """Convert all Customers to summary output model"""
        return CustomerSummaryOutputModel(customers_dict)

    @staticmethod
    def group_by_country(customers_dict):
        """Group customers by country"""
        return CustomersByCountryOutputModel(customers_dict)
