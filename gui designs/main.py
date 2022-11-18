import tkinter as tk
from navbar_container import NavbarContainerWidget
from user_info_container import UserInfoContainerWidget
from seperator_container import SeperatorContainerWidget
from data_display_container import DataDisplayContainerWidget

class Main(tk.Tk):
    def __init__(self, master=None, **kw):
        super(Main, self).__init__(master, **kw)
        enabled_test_data = True

        self.title("Healthcare Permanente - Insurance Billing")
        self.resizable(False, False)
        r = 0

        sep0_widget = SeperatorContainerWidget(self, show=False)
        sep0_widget.grid(column=0, row=r, pady=5)
        r += 1
        
        navbar_widget = NavbarContainerWidget(self)
        navbar_widget.grid(column=0, row=r)
        r += 1
        
        user_info_widget = UserInfoContainerWidget(self, test_data=enabled_test_data)
        user_info_widget.grid(column=0, row=r)
        r += 1
        
        sep1_widget = SeperatorContainerWidget(self)
        sep1_widget.grid(column=0, row=r, pady=10)
        r += 1
        
        data_display_container = DataDisplayContainerWidget(self, test_data=enabled_test_data)
        data_display_container.grid(column=0, row=r)
        r += 1
        
        sep2_widget = SeperatorContainerWidget(self, show=False)
        sep2_widget.grid(column=0, row=r, pady=5)
        r += 1
        
        gui_w, gui_h = 960, 720
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width/2) - (gui_w/2)
        y = (screen_height/2) - (gui_h/2)
        self.geometry('%dx%d+%d+%d' % (gui_w, gui_h, x, y))
        
        self.data = []
        
    def run(self):
        self.mainloop()
        
    def add_data(self, data):
        self.data.append(data)
        print(self.data)
    
if __name__ == "__main__":
    Main().run()