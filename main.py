import tkinter as tk
from model import Company
from view import CompanyView
from controller import CompanyController

if __name__ == "__main__":
    root = tk.Tk()
    company = Company()
    
    view = CompanyView(root)
    
    controller = CompanyController(company, view)
    
    view.setController(controller)
    
    root.mainloop()
