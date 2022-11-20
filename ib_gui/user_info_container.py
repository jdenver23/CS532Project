import tkinter as tk

class UserInfoContainerWidget(tk.Frame):
    def __init__(self, bill, master=None, test_data=False, **kw):
        super(UserInfoContainerWidget, self).__init__(master, **kw)
        self.bill = bill
        
        self.user_info_container = tk.Frame(self)
        self.user_info_container.configure(height=30, width=720)
        self.fr_user_info = tk.Frame(self.user_info_container)
        
        self.lb_user_id = tk.Label(self.fr_user_info)
        self.lb_user_id.configure(font="{Verdana} 8 {}", text='ID:')
        self.lb_user_id.pack(anchor="center", padx=10, side="left")
        
        self.user_id = tk.Text(self.fr_user_info)
        self.user_id.configure(
            background="SystemButtonFace",
            borderwidth=0,
            exportselection="true",
            font="{Verdana} 8 {}",
            height=1,
            state="disabled",
            width=8,
            wrap="char")
        _text_ = '12345678' if test_data else self.bill.user['ID']
        self.user_id.configure(state="normal")
        self.user_id.insert("0.0", _text_)
        self.user_id.configure(state="disabled")
        self.user_id.pack(anchor="center", side="left")
        
        self.lb_user_name = tk.Label(self.fr_user_info)
        self.lb_user_name.configure(
            anchor="e", font="{Verdana} 8 {}", text='Name:')
        self.lb_user_name.pack(anchor="center", ipadx=10, padx=10, side="left")
        
        self.user_name = tk.Text(self.fr_user_info)
        self.user_name.configure(
            background="SystemButtonFace",
            borderwidth=0,
            exportselection="true",
            font="{Verdana} 8 {}",
            height=1,
            state="disabled",
            width=10,
            wrap="word")
        _text_ = 'FIRST LAST' if test_data else self.bill.user_name
        self.user_name.configure(state="normal")
        self.user_name.insert("0.0", _text_)
        self.user_name.configure(state="disabled")
        self.user_name.pack(side="left")
        
        self.lb_user_address = tk.Label(self.fr_user_info)
        self.lb_user_address.configure(
            anchor="e", font="{Verdana} 8 {}", text='Address:')
        self.lb_user_address.pack(
            anchor="center",
            expand="false",
            ipadx=10,
            padx=10,
            side="left")
        
        self.user_address = tk.Text(self.fr_user_info)
        self.user_address.configure(
            background="SystemButtonFace",
            borderwidth=0,
            exportselection="true",
            font="{Verdana} 8 {}",
            height=1,
            state="disabled",
            width=20,
            wrap="word")
        _text_ = '12345 6TH BOULEVARD' if test_data else self.bill.user['Address']
        self.user_address.configure(state="normal")
        self.user_address.insert("0.0", _text_)
        self.user_address.configure(state="disabled")
        self.user_address.pack(side="left")
        
        self.lb_user_dob = tk.Label(self.fr_user_info)
        self.lb_user_dob.configure(
            anchor="e", font="{Verdana} 8 {}", text='DOB:')
        self.lb_user_dob.pack(
            anchor="center",
            expand="false",
            ipadx=10,
            padx=10,
            side="left")
        
        self.user_dob = tk.Text(self.fr_user_info)
        self.user_dob.configure(
            background="SystemButtonFace",
            borderwidth=0,
            exportselection="true",
            font="{Verdana} 8 {}",
            height=1,
            state="disabled",
            width=10,
            wrap="word")
        _text_ = '11/11/2011' if test_data else self.bill.user['Date of Birth']
        self.user_dob.configure(state="normal")
        self.user_dob.insert("0.0", _text_)
        self.user_dob.configure(state="disabled")
        self.user_dob.pack(side="left")
        
        self.fr_user_info.grid(column=0, row=0)
        
        self.user_info_container.grid(column=0, padx=10, row=0)
        self.user_info_container.grid_propagate(0)
        self.user_info_container.grid_anchor("center")
        self.configure(borderwidth=0)

    def set_text(self, text_widget, text="", index="0.0"):
        text_widget.insert(index, text)

if __name__ == "__main__":
    root = tk.Tk()
    widget = UserInfoContainerWidget(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

