from tkinter import messagebox

class CompanyController:
    def __init__(self, company, view):
        self.__company = company
        self.__view = view
        self.__currentOrder = None
        self.__loadInitialData()

    def __loadInitialData(self):
        # Load some sample customers and products
        c1 = self.__company.addCustomer("Ignacia Craft", 0)
        c2 = self.__company.addCustomer("Scarlett Wise", 0)
        c3 = self.__company.addCustomer("Fredericka Houston", 0)
        c4 = self.__company.addCustomer("Gage Rodgers", 0)
        c5 = self.__company.addCustomer("Gay Burris", 0)
        c6 = self.__company.addCustomer("Imogene Cruz", 0)
        c7 = self.__company.addCustomer("Karina Matthews", 0)
        c8 = self.__company.addCustomer("Dara McGee", 0)
        c9 = self.__company.addCustomer("Prescott Bowen", 0)
        c10 = self.__company.addCustomer("Samson Howell", 0)
        self.__view.setCustomerCombobox([c.customerName for c in self.__company.listAllCustomers()])

        p1 = self.__company.addProduct("Post-It Notes", 15.89)
        p2 = self.__company.addProduct("Blue Ballpoint Pens Box of 50", 32.65)
        p3 = self.__company.addProduct("Red Ballpoint Pens Box of 50", 32.65)
        p4 = self.__company.addProduct("Black Ballpoint Pens Box of 50", 32.65)
        p5 = self.__company.addProduct("Everyday Scissors 200mm", 21.85)
        p6 = self.__company.addProduct("Black Whiteboard Markers Pack of 6", 20.23)
        p7 = self.__company.addProduct("Red Whiteboard Markers Pack of 6", 20.23)
        p8 = self.__company.addProduct("Blue Whiteboard Markers Pack of 6", 20.23)
        p9 = self.__company.addProduct("White Copy Paper Pack of 500", 8.69)
        p10 = self.__company.addProduct("Full Strip Metal Stapler", 41.62)
        self.__view.setProductCombobox([p.productName for p in self.__company.listAllProducts()])

    def displayCustomerInfo(self, event):
        customerName = self.__view.getSelectedCustomer()
        customer = self.__company.findCustomer(customerName)
        if customer:
            info = (f"Customer ID: {customer.customerID}\n"
                    f"Customer Name: {customer.customerName}\n"
                    f"Balance: ${customer.customerBalance:.2f}\n")
            self.__view.updateCustomerInfo(info)
            self.__view.clearOrderDetails()

    def addProductToOrder(self):
        # check if there is a current order
        if not self.__currentOrder:
            customerName = self.__view.getSelectedCustomer()
            customer = self.__company.findCustomer(customerName)
            if customer:
                # create a new order for the selected customer
                self.__currentOrder = self.__company.addOrder(customer)
            else:
                messagebox.showwarning("Warning!", "Please select a customer!")
                return

        # check if there is a selected product and quantity
        productName = self.__view.getSelectedProduct()
        product = self.__company.findProduct(productName)
        if not product:
            messagebox.showwarning("Warning!", "Please select a product!")
            return

        quantity = self.__view.getQuantity()
        # check if quantity is valid
        if product and quantity is not None and quantity > 0:
            self.__currentOrder.addItem(product, quantity)
            details = f"{product.productName} - {product.productPrice} x {quantity} Subtotal: ${product.productPrice * quantity:.2f}\n"
            #clear order details
            self.__view.clearOrderDetails()
            #update order details
            self.__view.updateOrderDetails(details)
            #clear selected product and quantity
            self.__view.clearSelectedProduct()
            self.__view.resetQuantity()
        else:
            messagebox.showwarning("Warning!", "Please enter a valid quantity! Quantity must be a positive integer!")


    def submitOrder(self):
        # check if there is a current order and if there are items in the order
        if self.__currentOrder and self.__currentOrder.items:
            # set the balance of the customer to the total amount of the order
            self.__currentOrder.customer.customerBalance += self.__currentOrder.totalAmount
            messagebox.showinfo("Order Submitted", f"Order {self.__currentOrder.orderID} has been submitted.")
            # refresh customer info display
            self.displayCustomerInfo(None)
            # clear the product combobox
            self.__view.clearSelectedProduct()
            # reset the quantity
            self.__view.resetQuantity()
            # clear the order details
            self.__view.clearOrderDetails() 
            # clear the current order
            self.__currentOrder = None
        else:
            messagebox.showwarning("Warning!", "No current order found! Please make sure you have selected a customer and added products to the order.")


    def processPayment(self):
        customerName = self.__view.getSelectedCustomer()       
        customer = self.__company.findCustomer(customerName)
        # check if there is a selected customer
        if not customerName:
            messagebox.showwarning("Warning!", "Please select a customer!")
            return

        # check if there is a valid payment amount
        paymentAmount = self.__view.getPaymentAmount()
        if paymentAmount is None:
            messagebox.showwarning("Warning!", "Please enter a valid payment amount!")
            return
        
        # check if customer has a balance
        if customer.customerBalance <= 0:
            messagebox.showwarning("Warning!", f"{customer.customerName} has no outstanding balance!")
            return
        # check if payment amount is greater than customer balance
        if paymentAmount > customer.customerBalance:
            messagebox.showwarning("Warning!", "Payment amount is greater than customer balance!")
            return
        
        # Ask for confirmation before processing the payment
        confirm = messagebox.askokcancel(
            "Confirm Payment", 
            f"Are you sure you want to process the payment of ${paymentAmount:.2f} for {customer.customerName}?"
        )
        
        if confirm:
            # process payment
            success = self.__company.addPayment(customer, paymentAmount)
            if success:
                messagebox.showinfo("Payment Processed", f"Payment of {paymentAmount:.2f} processed for {customer.customerName}.")
                self.displayCustomerInfo(None)
                #clear payment amount
                self.__view.clearPaymentAmount()
            else:
                messagebox.showwarning("Warning!", "There was an issue processing the payment. Please try again.")
        else:
            messagebox.showinfo("Payment Cancelled", "Payment has been cancelled.")
            
    def listCustomerOrders(self):
        customerName = self.__view.getSelectedCustomer()
        customer = self.__company.findCustomer(customerName)
        if customer:
            orders = self.__company.listOrders(customer)
            # check if there are orders
            if not orders:
                #clear order details
                self.__view.clearOrderDetails()

                self.__view.updateOrderDetails("No orders found.")
                return
            
            self.__view.clearOrderDetails()
            for order in orders:
                formattedOrderDate = order.orderDate.strftime("%d %B %Y %H:%M:%S")
                details = f"Order ID: {order.orderID}, Date: {formattedOrderDate}, Total: ${order.totalAmount:.2f}\n"
                self.__view.updateOrderDetails(details)
        else:
            messagebox.showwarning("Warning!", "Please select a customer!")
              
    def listCustomerPayments(self):
        customerName = self.__view.getSelectedCustomer()
        customer = self.__company.findCustomer(customerName)
        if customer:
            payments = self.__company.listPayments(customer)
            # check if there are payments
            if not payments:
                #clear order details
                self.__view.clearOrderDetails()

                self.__view.updateOrderDetails("No payments found.")
                return
            
            self.__view.clearOrderDetails()
            for payment in payments:
                formattedPaymentDate = payment.paymentDate.strftime("%d %B %Y %H:%M:%S")
                details = f"Payment Date: {formattedPaymentDate}, Amount: ${payment.paymentAmount:.2f}\n"
                self.__view.updateOrderDetails(details)
        else:
            messagebox.showwarning("Warning!", "Please select a customer!")

    def listAllCustomers(self):
        self.__view.clearOrderDetails()
        customers = self.__company.listAllCustomers()
        # check if there are customers
        if not customers:
            #clear order details
            self.__view.clearOrderDetails()

            self.__view.updateOrderDetails("No customers found.")
            return
        
        for customer in customers:
            details = f"Customer ID: {customer.customerID}, Name: {customer.customerName}, Balance: ${customer.customerBalance:.2f}\n"
            self.__view.updateOrderDetails(details)

    def listAllOrders(self):
        self.__view.clearOrderDetails()
        orders = self.__company.listAllOrders()
        # check if there are orders
        if not orders:
            #clear order details
            self.__view.clearOrderDetails()
            self.__view.updateOrderDetails("No orders found.")
            return
        
        for order in orders:
            details = f"Order ID: {order.orderID}, Customer: {order.customer.customerName}, Total: ${order.totalAmount:.2f}\n"
            self.__view.updateOrderDetails(details)

    def listAllPayments(self):
        self.__view.clearOrderDetails()
        payments = self.__company.listAllPayments()
        # check if there are payments
        if not payments:
            #clear order details
            self.__view.clearOrderDetails()

            self.__view.updateOrderDetails("No payments found.")
            return
        
        for payment in payments:
            # format payment date
            formattedPaymentDate = payment.paymentDate.strftime("%d %B %Y %H:%M:%S")
            details = f"Payment Date: {formattedPaymentDate}, Customer: {payment.customer.customerName}, Amount: ${payment.paymentAmount:.2f}\n"
            self.__view.updateOrderDetails(details)
