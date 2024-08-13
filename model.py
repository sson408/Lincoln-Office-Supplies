from datetime import datetime

class Customer:

    def __init__(self, id, name, balance, nextId):
        self.customerID = id
        self.customerName = name
        self.customerBalance = balance
        self.nextId = nextId
        self.orders = []
        self.payments = []

class Product:
    def __init__(self, name, price):
        self.productName = name
        self.productPrice = price

class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

class Order:
    order_counter = 10000

    def __init__(self, customer):
        self.orderID = Order.order_counter
        Order.order_counter += 1
        self.customer = customer
        self.orderDate = datetime.now()
        self.items = []
        self.totalAmount = 0.0

    def add_item(self, product, quantity):
        order_item = OrderItem(product, quantity)
        self.items.append(order_item)
        self.totalAmount += product.productPrice * quantity

class Payment:
    def __init__(self, customer, amount):
        self.customer = customer
        self.paymentAmount = amount
        self.paymentDate = datetime.now()

class Company:
    def __init__(self):
        self.customers = []
        self.products = []

    def add_customer(self, name, balance):
        customer = Customer(name, balance)
        self.customers.append(customer)
        return customer

    def add_product(self, name, price):
        product = Product(name, price)
        self.products.append(product)
        return product

    def find_customer(self, name):
        for customer in self.customers:
            if customer.customerName == name:
                return customer
        return None

    def find_product(self, name):
        for product in self.products:
            if product.productName == name:
                return product
        return None

    def add_order(self, customer):
        order = Order(customer)
        customer.orders.append(order)
        return order

    def add_payment(self, customer, amount):
        payment = Payment(customer, amount)
        customer.payments.append(payment)
        customer.customerBalance -= amount

    def list_orders(self, customer):
        return customer.orders

    def list_payments(self, customer):
        return customer.payments

    def list_all_customers(self):
        return self.customers

    def list_all_orders(self):
        orders = []
        for customer in self.customers:
            orders.extend(customer.orders)
        return orders

    def list_all_payments(self):
        payments = []
        for customer in self.customers:
            payments.extend(customer.payments)
        return payments
