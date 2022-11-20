import tkinter as tk
from tkinter import messagebox
from .utils import tk_center
from .navbar_container import NavbarContainerWidget
from .user_info_container import UserInfoContainerWidget
from .seperator_container import SeperatorContainerWidget
from .data_display_container import DataDisplayContainerWidget

# TODO: check uid for security

class MainGUI(tk.Tk):
    def __init__(self, bill, master=None, enabled_test_data=False, **kw):
        # assert bill is not None, f"Invalid `InsuranceBilling` class instance."
        super(MainGUI, self).__init__(master, **kw)
        self.bill = bill
        self.master = master
        
        self.title("Healthcare Permanente - Insurance Billing")
        self.resizable(False, False)
        r = 0

        self.sep0_widget = SeperatorContainerWidget(self, show=False)
        self.sep0_widget.grid(column=0, row=r, pady=5)
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
        
        self.data_display_widget = DataDisplayContainerWidget(master=self, bill=self.bill, test_data=enabled_test_data)
        self.data_display_widget.grid(column=0, row=r)
        r += 1
        
        self.sep2_widget = SeperatorContainerWidget(self, show=False)
        self.sep2_widget.grid(column=0, row=r, pady=5)
        r += 1
        
        self.wm_protocol("WM_DELETE_WINDOW", self.on_closing)
        
        gui_w, gui_h = 960, 720
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
        