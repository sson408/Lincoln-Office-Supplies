import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CompanyView:
    def __init__(self, root, controller=None):
        self.controller = controller
        self.root = root
        self.root.title("Lincoln Office Supplies")
        self.root.geometry('600x670')

        root.columnconfigure(1, weight=1)

        # Customer Selection
        self.customer_var = tk.StringVar()
        tk.Label(root, text="Select Customer").grid(row=0, column=0, padx=10, pady=10)
      
        self.customer_combo = ttk.Combobox(root, textvariable=self.customer_var, state="readonly", width=40)
        self.customer_combo.grid(row=0, column=1, columnspan=5, padx=10, pady=10, sticky='e')
        self.customer_info = tk.Text(root, height=4, width=100, bg="#acf4f4")
        self.customer_info.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        # Process Order
        self.product_var = tk.StringVar()
        tk.Label(root, text="Process Order").grid(row=2, column=0, padx=10, pady=10)
        self.product_combo = ttk.Combobox(root, textvariable=self.product_var, state="readonly", width=40)
        self.product_combo.grid(row=2, column=1, columnspan=5,  padx=10, pady=10, sticky='e')

        self.quantity_var = tk.IntVar(value=1)
        tk.Label(root, text="Quantity").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.quantity_var).grid(row=3, column=1, columnspan=5, padx=10, pady=10, sticky='e')

        tk.Button(root, text="Add Product", command=self.controller.add_product_to_order if self.controller else None).grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky='e')

        self.order_details = tk.Text(root, height=10, width=100, bg="#acf4f4")
        self.order_details.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

        tk.Button(root, text="Submit Order", command=self.controller.submit_order if self.controller else None).grid(row=6, column=0, columnspan=5, padx=10, pady=10, sticky='e')

        # Process Payment
        self.payment_var = tk.DoubleVar()
        tk.Label(root, text="Process Payment").grid(row=7, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.payment_var).grid(row=7, column=1, columnspan=5, padx=10, pady=10, sticky='e')
        tk.Button(root, text="Pay", command=self.controller.process_payment if self.controller else None).grid(row=8, column=0, columnspan=5, padx=10, pady=10, sticky='e')

        # Reports
        tk.Button(root, text="List Customer Orders", command=self.controller.list_customer_orders if self.controller else None).grid(row=9, column=0, padx=10, pady=10)
        tk.Button(root, text="List Customer Payments", command=self.controller.list_customer_payments if self.controller else None).grid(row=9, column=1, padx=0, pady=10, sticky='w')
        tk.Button(root, text="List All Customers", command=self.controller.list_all_customers if self.controller else None).grid(row=9, column=2, padx=0, pady=10, sticky='w')
        tk.Button(root, text="List All Orders", command=self.controller.list_all_orders if self.controller else None).grid(row=9, column=3, padx=0, pady=0, sticky='w')
        tk.Button(root, text="List All Payments", command=self.controller.list_all_payments if self.controller else None).grid(row=9, column=4, padx=10, pady=10, sticky='e')

        # Exit
        tk.Button(root, text="Exit", command=root.quit).grid(row=12, column=0, columnspan=5, padx=10, pady=10, sticky='e')

    def update_customer_info(self, info):
        self.customer_info.delete(1.0, tk.END)
        self.customer_info.insert(tk.END, info)

    def update_order_details(self, details):
        self.order_details.insert(tk.END, details)

    def clear_order_details(self):
        self.order_details.delete(1.0, tk.END)

    def set_customer_combobox(self, values):
        self.customer_combo['values'] = values

    def set_product_combobox(self, values):
        self.product_combo['values'] = values

    def get_selected_customer(self):
        return self.customer_var.get()

    def get_selected_product(self):
        return self.product_var.get()

    def get_quantity(self):
        try:
            # get the quantity value and make sure it is an positive integer
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be a positive integer")        
            return quantity
        except (ValueError, tk.TclError):
            messagebox.showwarning("Invalid Quantity", "Please enter a valid quantity greater than zero.")
            return None

    def get_payment_amount(self):
        # need to check if the payment amount is a valid number
        try:
            payment_input = self.payment_var.get()
            # check if payment amount is empty
            if not payment_input:
                messagebox.showwarning("Invalid Payment Amount", "Please enter a payment amount.")
                return None
            
            payment_amount = float(payment_input)
            if payment_amount <= 0:
                raise ValueError("Payment amount must be a positive number.")
            return payment_amount
        except (ValueError, tk.TclError):
            messagebox.showwarning("Invalid Payment Amount", "Please enter a valid payment amount greater than zero.")
            return None
        

    def set_controller(self, controller):
        self.controller = controller
        self.customer_combo.bind("<<ComboboxSelected>>", self.controller.display_customer_info)
        # Update button commands
        self.root.grid_slaves(row=4, column=0)[0].config(command=self.controller.add_product_to_order)
        self.root.grid_slaves(row=6, column=0)[0].config(command=self.controller.submit_order)
        self.root.grid_slaves(row=8, column=0)[0].config(command=self.controller.process_payment)
        self.root.grid_slaves(row=9, column=0)[0].config(command=self.controller.list_customer_orders)
        self.root.grid_slaves(row=9, column=1)[0].config(command=self.controller.list_customer_payments)
        self.root.grid_slaves(row=9, column=2)[0].config(command=self.controller.list_all_customers)
        self.root.grid_slaves(row=9, column=3)[0].config(command=self.controller.list_all_orders)
        self.root.grid_slaves(row=9, column=4)[0].config(command=self.controller.list_all_payments)
