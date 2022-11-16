import tkinter as tk
import user_info_container
import navbar_container
import seperator_container

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    r = 0
    
    navbar_widget = navbar_container.NavbarContainerWidget(root)
    navbar_widget.grid(column=0, row=r)
    r += 1
    
    user_info_widget = user_info_container.UserInfoContainerWidget(root)
    user_info_widget.grid(column=0, row=r)
    r += 1
    
    sep1_widget = seperator_container.SeperatorContainerWidget(root)
    sep1_widget.grid(column=0, row=r)
    r += 1
    
    root.mainloop()