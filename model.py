from datetime import datetime

class Customer:
    __nextId = 1000
    def __init__(self, name, balance):
        self.__customerID = Customer.__nextId
        Customer.__nextId += 1
        self.__customerName = name
        self.__customerBalance = balance
        self.__orders = []
        self.__payments = []

    @property
    def customerID(self):
        return self.__customerID

    @property
    def customerName(self):
        return self.__customerName
    
    @property
    def customerBalance(self):
        return self.__customerBalance
    
    @customerBalance.setter
    def customerBalance(self, value):
        self.__customerBalance = value
 
    @property
    def orders(self):
        return self.__orders
    
    @property
    def payments(self):
        return self.__payments    

    def addOrder(self, order):
        self.__orders.append(order)

    def addPayment(self, payment):
        self.__payments.append(payment)


class Product:
    def __init__(self, name, price):
        self.__productName = name
        self.__productPrice = price

    @property
    def productName(self):
        return self.__productName

    @property
    def productPrice(self):
        return self.__productPrice  

class OrderItem:
    def __init__(self, product, quantity):
        self.__product = product
        self.__quantity = quantity

    @property
    def product(self):
        return self.__product

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value                   

class Order:
    __orderCounter = 10000

    def __init__(self, customer):
        self.__orderID = Order.__orderCounter
        Order.__orderCounter += 1
        self.__customer = customer
        self.__orderDate = datetime.now()
        self.__items = []
        self.__totalAmount = 0.0

    @property
    def orderID(self):
        return self.__orderID
    
    @property
    def customer(self):
        return self.__customer
    
    @property
    def orderDate(self):
        return self.__orderDate
    
    @property
    def items(self):
        return self.__items
    
    @property
    def totalAmount(self):
        return self.__totalAmount

    def addItem(self, product, quantity):
        orderItem = OrderItem(product, quantity)
        self.__items.append(orderItem)
        self.__totalAmount += product.productPrice * quantity

class Payment:
    def __init__(self, customer, amount):
        self.__customer = customer
        self.__paymentAmount = amount
        self.__paymentDate = datetime.now()

    @property
    def customer(self):
        return self.__customer
    
    @property
    def paymentAmount(self):
        return self.__paymentAmount
    
    @property
    def paymentDate(self):
        return self.__paymentDate

class Company:
    def __init__(self):
        self.__customers = []
        self.__products = []

    def addCustomer(self, name, balance):
        customer = Customer(name, balance)
        self.__customers.append(customer)
        return customer

    def addProduct(self, name, price):
        product = Product(name, price)
        self.__products.append(product)
        return product

    def findCustomer(self, name):
        for customer in self.__customers:
            if customer.customerName == name:
                return customer
        return None

    def findProduct(self, name):
        for product in self.__products:
            if product.productName == name:
                return product
        return None

    def addOrder(self, customer):
        order = Order(customer)
        customer.addOrder(order)
        return order

    def addOrderItem(self, order, product, quantity):
        if order and product and quantity > 0:
            order.addItem(product, quantity)
        else:
            raise ValueError("Invalid order, product, or quantity.")

    def addPayment(self, customer, amount):
        payment = Payment(customer, amount)
        customer.addPayment(payment)
        # check if customer has enough balance to process payment
        if customer.customerBalance >= amount:
            # deduct payment amount from customer balance
            customer.customerBalance -= amount
            return True
        else:
            # return False if customer does not have enough balance
            return False
        
    def listOrders(self, customer):
        return customer.orders

    def listPayments(self, customer):
        return customer.payments

    def listAllCustomers(self):
        return self.__customers
    
    def listAllProducts(self):
        return self.__products

    def listAllOrders(self):
        orders = []
        for customer in self.__customers:
            orders.extend(customer.orders)
        return orders

    def listAllPayments(self):
        payments = []
        for customer in self.__customers:
            payments.extend(customer.payments)
        return payments
