import tkinter as tk
from tkinter import messagebox
from enum import Enum
from .utils import tk_center, UIMode
from .navbar_container import NavbarContainerWidget
from .user_info_container import UserInfoContainerWidget
from .seperator_container import SeperatorContainerWidget
from .data_display_container_employee import DataDisplayContainerEmployeeWidget
from .data_display_container_user import DataDisplayContainerUserWidget
from InsuranceBilling import InsuranceBilling

EMPLOYEE_RANGE_L = 30000000
EMPLOYEE_RANGE_H = 40000000

ADMIN_IDS = ["1111"]

class MainGUI(tk.Tk):
    def __init__(self, bill: InsuranceBilling, master=None, enabled_test_data=False, **kw):
        super(MainGUI, self).__init__(master, **kw)
        self.bill = bill
        
        self.title("Insurance Billing - Healthcare Permanente (USER VIEW)")
        self.resizable(False, False)
        r = 0
        
        self.ui_mode = UIMode.PATIENT
        
        if self.bill.id >= EMPLOYEE_RANGE_L and self.bill.id < EMPLOYEE_RANGE_H or str(self.bill.id) in ADMIN_IDS:
            self.title("Insurance Billing - Healthcare Permanente (EMPLOYEE VIEW)")
            self.ui_mode = UIMode.EMPLOYEE
            
        self.sep0_widget = SeperatorContainerWidget(self, show=False)
        self.sep0_widget.grid(column=0, row=r)
        r += 1
        
        self.navbar_widget = NavbarContainerWidget(master=self, bill=bill)
        self.navbar_widget.grid(column=0, row=r)
        r += 1
        
        self.user_info_widget = UserInfoContainerWidget(master=self, bill=self.bill, test_data=enabled_test_data)
        self.user_info_widget.grid(column=0, row=r)
        r += 1
        
        self.sep1_widget = SeperatorContainerWidget(self)
        self.sep1_widget.grid(column=0, row=r, pady=10)
        r += 1
        
        # EMPLOYEE GUI VIEW
        if self.ui_mode == UIMode.EMPLOYEE:
            self.data_display_widget = DataDisplayContainerEmployeeWidget(master=self, bill=self.bill, test_data=enabled_test_data)
            self.data_display_widget.grid(column=0, row=r)
            r += 1
            
        # PATIENT GUI VIEW
        else:
            self.data_display_widget = DataDisplayContainerUserWidget(master=self, bill=self.bill, test_data=enabled_test_data)
            self.data_display_widget.grid(column=0, row=r)
            r += 1
        
            
        self.sep2_widget = SeperatorContainerWidget(self, show=False)
        self.sep2_widget.grid(column=0, row=r)
        r += 1
            
        self.wm_protocol("WM_DELETE_WINDOW", self.on_closing)
        
        gui_w, gui_h = 960, 680
        tk_center(self, gui_w, gui_h)
        
    def run(self):
        self.mainloop()
    
    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()
    
    def calls(self, widget_name):
        if widget_name == "nbc":
            return self.navbar_widget
        if widget_name == "uic":
            return self.user_info_widget
        if widget_name == "ddc":
            return self.data_display_widget
        