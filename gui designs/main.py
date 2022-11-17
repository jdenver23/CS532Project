import tkinter as tk
from navbar_container import NavbarContainerWidget
from user_info_container import UserInfoContainerWidget
from seperator_container import SeperatorContainerWidget
from data_display_container import DataDisplayContainerWidget

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Healthcare Permanente")
    root.resizable(False, False)
    r = 0

    sep0_widget = SeperatorContainerWidget(root, show=False)
    sep0_widget.grid(column=0, row=r, pady=5)
    r += 1
    
    navbar_widget = NavbarContainerWidget(root)
    navbar_widget.grid(column=0, row=r)
    r += 1
    
    user_info_widget = UserInfoContainerWidget(root)
    user_info_widget.grid(column=0, row=r)
    r += 1
    
    sep1_widget = SeperatorContainerWidget(root)
    sep1_widget.grid(column=0, row=r, pady=10)
    r += 1
    
    data_display_container = DataDisplayContainerWidget(root)
    data_display_container.grid(column=0, row=r)
    r += 1
    
    sep2_widget = SeperatorContainerWidget(root, show=False)
    sep2_widget.grid(column=0, row=r, pady=5)
    r += 1
    
    root.mainloop()