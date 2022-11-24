import tkinter as tk
from tkinter import messagebox
from .utils import tk_center, UIMode, EMPLOYEE_RANGE_L, EMPLOYEE_RANGE_H
from .navbar_container import NavbarContainerWidget
from .user_info_container import UserInfoContainerWidget
from .seperator_container import SeperatorContainerWidget
from .data_display_container_employee import DataDisplayContainerEmployeeWidget
from .data_display_container_user import DataDisplayContainerUserWidget
from InsuranceBilling import InsuranceBilling

ADMIN_IDS = ["1111"]

class MainGUI(tk.Tk):
    def __init__(self, bill: InsuranceBilling, master=None, enabled_test_data=False, **kw):
        super(MainGUI, self).__init__(master, **kw)
        self.bill = bill
        
        self.title("Insurance Billing - Healthcare Permanente (USER VIEW)")
        self.resizable(False, False)
        r = 0
        
        self.ui_mode = UIMode.PATIENT
        
        if int(self.bill.id) >= EMPLOYEE_RANGE_L and int(self.bill.id) < EMPLOYEE_RANGE_H or str(self.bill.id) in ADMIN_IDS:
            self.title("Insurance Billing - Healthcare Permanente (EMPLOYEE VIEW)")
            self.ui_mode = UIMode.EMPLOYEE
            
        self.sep0_widget = SeperatorContainerWidget(self, show=False)
        self.sep0_widget.grid(column=0, row=r)
        r += 1
        
        self.navbar_widget = NavbarContainerWidget(master=self, bill=bill, ui_mode=self.ui_mode)
        self.navbar_widget.grid(column=0, row=r)
        r += 1
        
        self.user_info_widget = UserInfoContainerWidget(master=self, bill=self.bill, test_data=enabled_test_data)
        self.user_info_widget.grid(column=0, row=r)
        r += 1
        
        self.sep1_widget = SeperatorContainerWidget(self)
        self.sep1_widget.grid(column=0, row=r, pady=10)
        r += 1
        
        # EMPLOYEE GUI VIEW
        if self.ui_mode is UIMode.EMPLOYEE:        
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
        
        gui_w, gui_h = 960, 690
        tk_center(self, gui_w, gui_h)
        
        self.navbar_widget.def_calls()
        
    def run(self):
        self.mainloop()
    
    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()
    
    def calls(self, widget_name):
        """ Return specified widget reference. """
        if widget_name == "nbc" and hasattr(self, "navbar_widget"):
            return self.navbar_widget
        if widget_name == "uic" and hasattr(self, "user_info_widget"):
            return self.user_info_widget
        if widget_name == "ddc" and hasattr(self, "data_display_widget"):
            return self.data_display_widget
        