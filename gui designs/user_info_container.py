import tkinter as tk

class UserInfoContainerWidget(tk.Frame):
    def __init__(self, master=None, **kw):
        super(UserInfoContainerWidget, self).__init__(master, **kw)
        self.user_info_container = tk.Frame(self)
        self.user_info_container.configure(height=30, width=720)
        self.fr_user_info = tk.Frame(self.user_info_container)
        self.lb_user_id = tk.Label(self.fr_user_info)
        self.lb_user_id.configure(
            anchor="e",
            font="{Verdana} 8 {}",
            justify="left",
            text='ID:')
        self.lb_user_id.pack(anchor="center", padx=10, side="left")
        self.user_id_text = tk.Label(self.fr_user_info)
        self.user_id_text.configure(
            background="#dadada",
            font="{Verdana} 8 {}",
            text='12345678')
        self.user_id_text.pack(anchor="center", expand="true", side="left")
        self.lb_user_name = tk.Label(self.fr_user_info)
        self.lb_user_name.configure(
            anchor="e",
            font="{Verdana} 8 {}",
            justify="left",
            text='Name:')
        self.lb_user_name.pack(anchor="center", ipadx=10, padx=10, side="left")
        self.user_name_text = tk.Label(self.fr_user_info)
        self.user_name_text.configure(
            background="#dadada",
            font="{Verdana} 8 {}",
            justify="center",
            relief="flat",
            text='First Last')
        self.user_name_text.pack(anchor="center", expand="true", side="left")
        self.lb_user_address = tk.Label(self.fr_user_info)
        self.lb_user_address.configure(
            anchor="e",
            font="{Verdana} 8 {}",
            justify="left",
            text='Address:')
        self.lb_user_address.pack(
            anchor="center",
            expand="false",
            ipadx=10,
            padx=10,
            side="left")
        self.user_address_text = tk.Label(self.fr_user_info)
        self.user_address_text.configure(
            background="#dadada",
            font="{Verdana} 8 {}",
            height=1,
            justify="left",
            relief="flat",
            state="normal",
            text='12345 6th Boulevard',
            wraplength=120)
        self.user_address_text.pack(
            anchor="center", expand="true", side="left")
        self.lb_user_dob = tk.Label(self.fr_user_info)
        self.lb_user_dob.configure(
            anchor="e",
            font="{Verdana} 8 {}",
            justify="left",
            text='DOB:')
        self.lb_user_dob.pack(
            anchor="center",
            expand="false",
            ipadx=10,
            padx=10,
            side="left")
        self.user_dob_text = tk.Label(self.fr_user_info)
        self.user_dob_text.configure(
            anchor="w",
            background="#dadada",
            font="{Verdana} 8 {}",
            justify="left",
            text='11/11/1111')
        self.user_dob_text.pack(anchor="center", expand="true", side="left")
        self.fr_user_info.grid(column=0, row=0)
        self.user_info_container.grid(column=0, padx=10, row=0)
        self.user_info_container.grid_propagate(0)
        self.user_info_container.grid_anchor("center")
        self.configure(borderwidth=0)

if __name__ == "__main__":
    root = tk.Tk()
    widget = UserInfoContainerWidget(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

