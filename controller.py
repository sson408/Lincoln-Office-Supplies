from tkinter import messagebox

class CompanyController:
    def __init__(self, company, view):
        self.company = company
        self.view = view
        self.current_order = None
        self.load_initial_data()

    def load_initial_data(self):
        # Load some sample customers and products
        c1 = self.company.add_customer("Ignacia Craft", 0)
        c2 = self.company.add_customer("Scarlett Wise", 0)
        c3 = self.company.add_customer("Fredericka Houston", 0)
        c4 = self.company.add_customer("Gage Rodgers", 0)
        c5 = self.company.add_customer("Gay Burris", 0)
        c6 = self.company.add_customer("Imogene Cruz", 0)
        c7 = self.company.add_customer("Karina Matthews", 0)
        c8 = self.company.add_customer("Dara McGee", 0)
        c9 = self.company.add_customer("Prescott Bowen", 0)
        c10 = self.company.add_customer("Samson Howell", 0)
        self.view.set_customer_combobox([c.customerName for c in self.company.customers])
        
        p1 = self.company.add_product("Post-It Notes", 15.89)
        p2 = self.company.add_product("Blue Ballpoint Pens Box of 50", 32.65)
        p3 = self.company.add_product("Red Ballpoint Pens Box of 50", 32.65)
        p4 = self.company.add_product("Black Ballpoint Pens Box of 50", 32.65)
        p5 = self.company.add_product("Everyday Scissors 200mm", 21.85)
        p6 = self.company.add_product("Black Whiteboard Markers Pack of 6", 20.23)
        p7 = self.company.add_product("Red Whiteboard Markers Pack of 6", 20.23)
        p8 = self.company.add_product("Blue Whiteboard Markers Pack of 6", 20.23)
        p9 = self.company.add_product("White Copy Paper Pack of 500", 8.69)
        p10 = self.company.add_product("Full Strip Metal Stapler", 41.62)
        self.view.set_product_combobox([p.productName for p in self.company.products])

    def display_customer_info(self, event):
        customer_name = self.view.get_selected_customer()
        customer = self.company.find_customer(customer_name)
        if customer:
            info = (f"Customer ID: {customer.customerID}\n"
                    f"Customer Name: {customer.customerName}\n"
                    f"Balance: {customer.customerBalance:.2f}\n")
            self.view.update_customer_info(info)
            self.current_order = self.company.add_order(customer) 
            self.view.clear_order_details()

    def add_product_to_order(self):
        if self.current_order:
            product_name = self.view.get_selected_product()
            product = self.company.find_product(product_name)
            quantity = self.view.get_quantity()
            if product and quantity > 0:
                self.current_order.add_item(product, quantity)
                details = f"{product.productName} x{quantity} Subtotal: {product.productPrice * quantity:.2f}\n"
                self.view.update_order_details(details)
            else:
                print("Invalid product or quantity.")
        else:
            print("No current order found.")

    def submit_order(self):
        if self.current_order:
            self.current_order.customer.customerBalance += self.current_order.totalAmount
            messagebox.showinfo("Order Submitted", f"Order {self.current_order.orderID} has been submitted.")
            self.current_order = None

    def process_payment(self):
        customer_name = self.view.get_selected_customer()
        customer = self.company.find_customer(customer_name)
        payment_amount = self.view.get_payment_amount()
        if customer and payment_amount > 0:
            self.company.add_payment(customer, payment_amount)
            messagebox.showinfo("Payment Processed", f"Payment of {payment_amount:.2f} processed for {customer.customerName}.")
            self.display_customer_info(None)  # Refresh customer info display

    def list_customer_orders(self):
        customer_name = self.view.get_selected_customer()
        customer = self.company.find_customer(customer_name)
        if customer:
            orders = self.company.list_orders(customer)
            self.view.clear_order_details()
            for order in orders:
                details = f"Order ID: {order.orderID} Date: {order.orderDate} Total: {order.totalAmount:.2f}\n"
                self.view.update_order_details(details)

    def list_customer_payments(self):
        customer_name = self.view.get_selected_customer()
        customer = self.company.find_customer(customer_name)
        if customer:
            payments = self.company.list_payments(customer)
            self.view.clear_order_details()
            for payment in payments:
                details = f"Payment Date: {payment.paymentDate} Amount: {payment.paymentAmount:.2f}\n"
                self.view.update_order_details(details)

    def list_all_customers(self):
        self.view.clear_order_details()
        customers = self.company.list_all_customers()
        for customer in customers:
            details = f"Customer ID: {customer.customerID} Name: {customer.customerName} Balance: {customer.customerBalance:.2f}\n"
            self.view.update_order_details(details)

    def list_all_orders(self):
        self.view.clear_order_details()
        orders = self.company.list_all_orders()
        for order in orders:
            details = f"Order ID: {order.orderID} Customer: {order.customer.customerName} Total: {order.totalAmount:.2f}\n"
            self.view.update_order_details(details)

    def list_all_payments(self):
        self.view.clear_order_details()
        payments = self.company.list_all_payments()
        for payment in payments:
            details = f"Payment Date: {payment.paymentDate} Customer: {payment.customer.customerName} Amount: {payment.paymentAmount:.2f}\n"
            self.view.update_order_details(details)
