import tkinter as tk
from tkinter import ttk

class CompanyView:
    def __init__(self, root, controller=None):
        self.__controller = controller
        self.__root = root
        self.__root.title("Lincoln Office Supplies")
        self.__root.geometry('600x670')

        self.__root.columnconfigure(1, weight=1)

        # Customer Selection
        self.__customerVar = tk.StringVar()
        tk.Label(root, text="Select Customer").grid(row=0, column=0, padx=10, pady=10)
      
        self.__customerCombo = ttk.Combobox(root, textvariable=self.__customerVar, state="readonly", width=40)
        self.__customerCombo.grid(row=0, column=1, columnspan=5, padx=10, pady=10, sticky='e')
        self.__customerInfo = tk.Text(root, height=4, width=100, bg="#acf4f4")
        self.__customerInfo.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        # Process Order
        self.__productVar = tk.StringVar()
        tk.Label(root, text="Process Order").grid(row=2, column=0, padx=10, pady=10)
        self.__productCombo = ttk.Combobox(root, textvariable=self.__productVar, state="readonly", width=40)
        self.__productCombo.grid(row=2, column=1, columnspan=5,  padx=10, pady=10, sticky='e')

        validQuantity = (self.__root.register(self.__validateQuantity), '%P')

        self.__quantityVar = tk.IntVar(value=1)
        tk.Label(root, text="Quantity").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.__quantityVar, validate='key', validatecommand=validQuantity).grid(row=3, column=1, columnspan=5, padx=10, pady=10, sticky='e')

        tk.Button(root, text="Add Product", command=self.__controller.addProductToOrder if self.__controller else None).grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky='e')

        self.__orderDetails = tk.Text(root, height=10, width=100, bg="#acf4f4")
        self.__orderDetails.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

        tk.Button(root, text="Submit Order", command=self.__controller.submitOrder if self.__controller else None).grid(row=6, column=0, columnspan=5, padx=10, pady=10, sticky='e')

        # Process Payment
        self.__paymentVar = tk.DoubleVar()

        # Add validation command
        validPayment = (self.__root.register(self.__validatePayment), '%P')
        tk.Label(root, text="Process Payment").grid(row=7, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.__paymentVar, validate='key', validatecommand=validPayment).grid(row=7, column=1, columnspan=5, padx=10, pady=10, sticky='e')
        tk.Button(root, text="Pay", command=self.__controller.processPayment if self.__controller else None).grid(row=8, column=0, columnspan=5, padx=10, pady=10, sticky='e')

        # Reports
        tk.Button(root, text="List Customer Orders", command=self.__controller.listCustomerOrders if self.__controller else None).grid(row=9, column=0, padx=10, pady=10)
        tk.Button(root, text="List Customer Payments", command=self.__controller.listCustomerPayments if self.__controller else None).grid(row=9, column=1, padx=0, pady=10, sticky='w')
        tk.Button(root, text="List All Customers", command=self.__controller.listAllCustomers if self.__controller else None).grid(row=9, column=2, padx=0, pady=10, sticky='w')
        tk.Button(root, text="List All Orders", command=self.__controller.listAllOrders if self.__controller else None).grid(row=9, column=3, padx=0, pady=0, sticky='w')
        tk.Button(root, text="List All Payments", command=self.__controller.listAllPayments if self.__controller else None).grid(row=9, column=4, padx=10, pady=10, sticky='e')

        # Exit
        tk.Button(root, text="Exit", command=root.quit).grid(row=12, column=0, columnspan=5, padx=10, pady=10, sticky='e')
    
   # Validation function for quantity (must be a positive integer)
    def __validateQuantity(self, new_value):
        if new_value == "":
            return True
        if new_value.isdigit() and int(new_value) > 0:
            return True
        return False

    # Validation function for payment amount (max 2 decimal places)
    def __validatePayment(self, new_value):
        if new_value == "":
            return True  # Allow empty field
        try:
            # Check if the value is a valid float
            float_value = float(new_value)
            if float_value < 0:
                return False  # No negative numbers allowed
            
            # Check for two decimal places (only if there is a decimal point)
            if '.' in new_value and len(new_value.split('.')[-1]) > 2:
                return False
            
            return True
        except ValueError:
            return False  # If input is not a valid float
        
    def updateCustomerInfo(self, info):
        self.__customerInfo.delete(1.0, tk.END)
        self.__customerInfo.insert(tk.END, info)
    
    def updateOrderDetails(self, details):
        self.__orderDetails.insert(tk.END, details)

    def clearOrderDetails(self):
        self.__orderDetails.delete(1.0, tk.END)

    def setCustomerCombobox(self, values):
        self.__customerCombo['values'] = values

    def setProductCombobox(self, values):
        self.__productCombo['values'] = values

    def getSelectedCustomer(self):
        return self.__customerVar.get()

    def getSelectedProduct(self):
        return self.__productVar.get()
    
    def clearSelectedProduct(self):
        self.__productVar.set('')

    def resetQuantity(self):
        self.__quantityVar.set(1) 

    def getQuantity(self):
        try:
            quantity = int(self.__quantityVar.get())
            if quantity <= 0:
                raise ValueError("Quantity must be a positive integer")
            return quantity
        except (ValueError, tk.TclError):
            return None

    def getPaymentAmount(self):
        try:
            paymentInput = self.__paymentVar.get()
            if not paymentInput:
                return None

            paymentAmount = float(paymentInput)
            if paymentAmount <= 0:
                return None
            return paymentAmount
        except (ValueError, tk.TclError):
            return None
    def clearPaymentAmount(self):
        self.__paymentVar.set(0.0)

    def setController(self, controller):
        self.__controller = controller
        self.__customerCombo.bind("<<ComboboxSelected>>", self.__controller.displayCustomerInfo)
        self.__root.grid_slaves(row=4, column=0)[0].config(command=self.__controller.addProductToOrder)
        self.__root.grid_slaves(row=6, column=0)[0].config(command=self.__controller.submitOrder)
        self.__root.grid_slaves(row=8, column=0)[0].config(command=self.__controller.processPayment)
        self.__root.grid_slaves(row=9, column=0)[0].config(command=self.__controller.listCustomerOrders)
        self.__root.grid_slaves(row=9, column=1)[0].config(command=self.__controller.listCustomerPayments)
        self.__root.grid_slaves(row=9, column=2)[0].config(command=self.__controller.listAllCustomers)
        self.__root.grid_slaves(row=9, column=3)[0].config(command=self.__controller.listAllOrders)
        self.__root.grid_slaves(row=9, column=4)[0].config(command=self.__controller.listAllPayments)
