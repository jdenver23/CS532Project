import tkinter as tk
from tkinter import messagebox
from .utils import tk_center
from .navbar_container import NavbarContainerWidget
from .user_info_container import UserInfoContainerWidget
from .seperator_container import SeperatorContainerWidget
from .data_display_container import DataDisplayContainerWidget

class MainGUI(tk.Tk):
    def __init__(self, bill, master=None, enabled_test_data=False, **kw):
        # assert bill is not None, f"Invalid `InsuranceBilling` class instance."
        super(MainGUI, self).__init__(master, **kw)
        self.bill = bill
        self.master = master
        
        self.title("Healthcare Permanente - Insurance Billing")
        self.resizable(False, False)
        r = 0

        sep0_widget = SeperatorContainerWidget(self, show=False)
        sep0_widget.grid(column=0, row=r, pady=5)
        r += 1
        
        navbar_widget = NavbarContainerWidget(master=self, bill=bill)
        navbar_widget.grid(column=0, row=r)
        r += 1
        
        user_info_widget = UserInfoContainerWidget(master=self, bill=self.bill, test_data=enabled_test_data)
        user_info_widget.grid(column=0, row=r)
        r += 1
        
        sep1_widget = SeperatorContainerWidget(self)
        sep1_widget.grid(column=0, row=r, pady=10)
        r += 1
        
        data_display_container = DataDisplayContainerWidget(master=self, bill=self.bill, test_data=enabled_test_data)
        data_display_container.grid(column=0, row=r)
        r += 1
        
        sep2_widget = SeperatorContainerWidget(self, show=False)
        sep2_widget.grid(column=0, row=r, pady=5)
        r += 1
        
        self.wm_protocol("WM_DELETE_WINDOW", self.on_closing)
        
        gui_w, gui_h = 960, 720
        tk_center(self, gui_w, gui_h)
        
    def run(self):
        self.mainloop()
    
    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()