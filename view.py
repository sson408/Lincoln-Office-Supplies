import tkinter as tk
from tkinter import ttk

class CompanyView:
    def __init__(self, root, controller=None):
        self.controller = controller
        self.root = root
        self.root.title("Lincoln Office Supplies")

        # Customer Selection
        self.customer_var = tk.StringVar()
        tk.Label(root, text="Select Customer").grid(row=0, column=0, padx=10, pady=10)
        self.customer_combo = ttk.Combobox(root, textvariable=self.customer_var, state="readonly")
        self.customer_combo.grid(row=0, column=1, padx=10, pady=10)

        self.customer_info = tk.Text(root, height=4, width=40)
        self.customer_info.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Process Order
        self.product_var = tk.StringVar()
        tk.Label(root, text="Process Order").grid(row=2, column=0, padx=10, pady=10)
        self.product_combo = ttk.Combobox(root, textvariable=self.product_var, state="readonly")
        self.product_combo.grid(row=2, column=1, padx=10, pady=10)

        self.quantity_var = tk.IntVar(value=1)
        tk.Label(root, text="Quantity").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.quantity_var).grid(row=3, column=1, padx=10, pady=10)

        tk.Button(root, text="Add Product", command=self.controller.add_product_to_order if self.controller else None).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.order_details = tk.Text(root, height=10, width=60)
        self.order_details.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        tk.Button(root, text="Submit Order", command=self.controller.submit_order if self.controller else None).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Process Payment
        self.payment_var = tk.DoubleVar()
        tk.Label(root, text="Process Payment").grid(row=7, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.payment_var).grid(row=7, column=1, padx=10, pady=10)
        tk.Button(root, text="Pay", command=self.controller.process_payment if self.controller else None).grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Reports
        tk.Button(root, text="List Customer Orders", command=self.controller.list_customer_orders if self.controller else None).grid(row=9, column=0, padx=10, pady=10)
        tk.Button(root, text="List Customer Payments", command=self.controller.list_customer_payments if self.controller else None).grid(row=9, column=1, padx=10, pady=10)
        tk.Button(root, text="List All Customers", command=self.controller.list_all_customers if self.controller else None).grid(row=10, column=0, padx=10, pady=10)
        tk.Button(root, text="List All Orders", command=self.controller.list_all_orders if self.controller else None).grid(row=10, column=1, padx=10, pady=10)
        tk.Button(root, text="List All Payments", command=self.controller.list_all_payments if self.controller else None).grid(row=11, column=0, columnspan=2, padx=10, pady=10)

        # Exit
        tk.Button(root, text="Exit", command=root.quit).grid(row=12, column=0, columnspan=2, padx=10, pady=10)

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
        return self.quantity_var.get()

    def get_payment_amount(self):
        return self.payment_var.get()

    def set_controller(self, controller):
        self.controller = controller
        self.customer_combo.bind("<<ComboboxSelected>>", self.controller.display_customer_info)
        # Update button commands
        self.root.grid_slaves(row=4, column=0)[0].config(command=self.controller.add_product_to_order)
        self.root.grid_slaves(row=6, column=0)[0].config(command=self.controller.submit_order)
        self.root.grid_slaves(row=8, column=0)[0].config(command=self.controller.process_payment)
        self.root.grid_slaves(row=9, column=0)[0].config(command=self.controller.list_customer_orders)
        self.root.grid_slaves(row=9, column=1)[0].config(command=self.controller.list_customer_payments)
        self.root.grid_slaves(row=10, column=0)[0].config(command=self.controller.list_all_customers)
        self.root.grid_slaves(row=10, column=1)[0].config(command=self.controller.list_all_orders)
        self.root.grid_slaves(row=11, column=0)[0].config(command=self.controller.list_all_payments)
