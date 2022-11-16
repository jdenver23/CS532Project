#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox

carriers = [['tree', '123st', 'PRIMARY'],
            ['jess', '456rd', 'NON-PRIMARY'],
            ['helo', '@elca', 'NON-PRIMARY']]

class InsurancebillingApp:
    def __init__(self, bill, root=None):
        self.bill = bill
        self.root = root
        self.gui_w = 600
        self.gui_h = 600
        # build ui
        self.ib_gui = tk.Frame(root)
        self.ib_gui.configure(
            background="grey",
            borderwidth=0,
            height=self.gui_h,
            width=self.gui_w)
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        x = (screen_width/2) - (self.gui_w/2)
        y = (screen_height/2) - (self.gui_h/2)
        self.root.geometry('%dx%d+%d+%d' % (self.gui_w, self.gui_h, x, y))
        
        self.user_info_container = tk.LabelFrame(self.ib_gui)
        self.user_info_container.configure(
            background="grey",
            font="{Verdana} 8 {}",
            height=50,
            text='Info',
            width=580)
        self.lb_user_id = tk.Label(self.user_info_container)
        self.lb_user_id.configure(
            background="grey",
            font="{Verdana} 8 {}",
            justify="left",
            text='ID:')
        self.lb_user_id.pack(
            anchor="center",
            expand="false",
            padx=10,
            side="left")
        self.lb_user_name = tk.Label(self.user_info_container)
        self.lb_user_name.configure(
            background="grey",
            font="{Verdana} 8 {}",
            justify="left",
            text='Name:')
        self.lb_user_name.pack(
            anchor="center",
            expand="false",
            padx=80,
            side="left")
        self.lb_user_address = tk.Label(self.user_info_container)
        self.lb_user_address.configure(
            background="grey",
            font="{Verdana} 8 {}",
            justify="left",
            text='Address:')
        self.lb_user_address.pack(
            anchor="center",
            expand="false",
            padx=50,
            side="left")
        self.lb_user_dob = tk.Label(self.user_info_container)
        self.lb_user_dob.configure(
            background="grey",
            font="{Verdana} 8 {}",
            justify="left",
            text='DOB:')
        self.lb_user_dob.pack(
            anchor="center",
            expand="false",
            padx=60,
            side="left")
        self.user_info_container.grid(
            column=0, padx=10, pady=10, row=0, sticky="nw")
        self.user_info_container.pack_propagate(0)
        
        self.carrier_container = tk.LabelFrame(self.ib_gui)
        self.carrier_container.configure(
            background="grey",
            font="{Verdana} 8 {}",
            height=150,
            text='Carrier',
            width=550)
        
        self.fr_carrier_info = tk.Frame(self.carrier_container)
        self.fr_carrier_info.configure(
            background="grey", height=200, width=200)
        self.fr_carrier_info.grid(column=0, ipadx=10, row=0)
        self.fr_carrier_info.grid_anchor("center")
        
        self.generate_carrier_info()
        
        self.carrier_container.grid(column=0, row=1)
        self.carrier_container.grid_propagate(0)
        self.carrier_container.grid_anchor("n")
        self.service_container = tk.LabelFrame(self.ib_gui)
        self.service_container.configure(
            background="grey",
            font="{Verdana} 8 {}",
            height=150,
            text='Service',
            width=500)
        self.service_container.grid(column=0, row=2)
        self.invoice_container = tk.LabelFrame(self.ib_gui)
        self.invoice_container.configure(
            background="grey",
            font="{Verdana} 8 {}",
            height=150,
            text='Invoice',
            width=500)
        self.invoice_container.grid(column=0, row=3)
        self.fr_gui_control = tk.Frame(self.ib_gui)
        self.fr_gui_control.configure(background="grey", height=50, width=500)
        self.btn_back_to_home = tk.Button(self.fr_gui_control)
        self.btn_back_to_home.configure(
            background="#2980b9",
            font="{Verdana} 12 {}",
            foreground="white",
            highlightbackground="black",
            highlightcolor="blue",
            relief="flat",
            text='⬅ Home',
            command=lambda: self.on_closing())
        self.btn_back_to_home.grid(column=0, padx=20, pady=10, row=0)
        self.btn_save_changes = tk.Button(self.fr_gui_control)
        self.btn_save_changes.configure(
            background="#2980b9",
            font="{Verdana} 12 {}",
            foreground="white",
            relief="flat",
            takefocus=True,
            text='Save Changes ✓',
            command=lambda: self.save_changes())
        self.btn_save_changes.grid(column=1, padx=20, pady=10, row=0)
        self.fr_gui_control.grid(column=0, pady=15, row=4)
        self.ib_gui.pack(side="top")
        self.ib_gui.grid_propagate(0)

        # Main widget
        self.mainwindow = self.ib_gui
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.local_changes_made = False

    def run(self):
        self.mainwindow.mainloop()

    def generate_carrier_info(self):
        carrier_field_names = ["Name", "Address", "Primary"]
        for i in range(3):
            lb_carrier_fields = tk.Label(self.fr_carrier_info)
            lb_carrier_fields.configure(
                background="grey",
                font="{Verdana} 8 {}",
                justify="center",
                text=f'{carrier_field_names[i]}')
            lb_carrier_fields.grid(column=i, padx=48, row=0)
            
        lb_carrier_fields = tk.Label(self.fr_carrier_info)
        lb_carrier_fields.configure(
            background="grey",
            font="{Verdana} 8 {}",
            justify="center",
            text='Action')
        lb_carrier_fields.grid(column=4, padx=2, row=0)
        
        self.fr_carrier_list = []
        for r in range(len(carriers)):
            fr_carrier_list_item = tk.Frame(self.carrier_container)
            fr_carrier_list_item.configure(background="grey", height=50, width=550)
            fr_carrier_list_item.grid(column=0, row=r+1)
            fr_carrier_list_item.grid_anchor("center")
            for c in range(3):
                # create carrier info using multiple entries on the same row
                entry_carrier_info = tk.Entry(fr_carrier_list_item)
                entry_carrier_info.configure(
                    font="{Verdana} 8 {}",
                    justify="center",
                    state="readonly")
                _text_ = f'{carriers[r][c]}'
                entry_carrier_info["state"] = "normal"
                entry_carrier_info.delete("0", "end")
                entry_carrier_info.insert("0", _text_)
                entry_carrier_info["state"] = "readonly"
                entry_carrier_info.grid(column=c, row=r, padx=1)
            
            # create carrier remove btns
            btn_remove_carrier = tk.Button(fr_carrier_list_item)
            btn_remove_carrier.configure(
                activeforeground="red",
                font="{Verdana} 7 {}",
                height=1,
                justify="center",
                text='X',
                width=1)
            btn_remove_carrier.grid(column=c+1, row=r, padx=10, ipadx=5)
            btn_remove_carrier.configure(command=lambda idx=r: self.remove_carrier(idx))
            self.fr_carrier_list.append(fr_carrier_list_item)
        
    def remove_carrier(self, idx):
        self.fr_carrier_list[idx].destroy()
        
    def remove_carrier(self, idx):
        self.fr_carrier_list[idx].destroy()
        self.local_changes_made = True

    def save_changes(self):
        self.local_changes_made = False
        print("changes saved to database")
    
    def on_closing(self):
        if self.local_changes_made:
            if messagebox.askokcancel("Quit", "You have unsaved changes. Are you sure you want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()

# TODO:
# - [ ] Carrier managing GUI
#   - [X] Remove carrier
#   - [ ] Add carrier
#   - [ ] Set primary carrier
#
# - [ ] Service managing GUI
#   - [ ] Remove service
#   - [ ] Add service
#
# - [ ] Invoice managing GUI
#   - [ ] Generate invoice for specific month
#   - [ ] Pay for invoice
#   - [ ] View all generated invoices
#
# - [ ] Report generating GUI
#   - [ ] Generate delinquent reports
#
# - [ ] Notification box (for invoice reminder?)
# - [ ] Reload from database button
# - [ ] Save changes button
# - [ ] Home button
if __name__ == "__main__":
    root = tk.Tk()
    app = InsurancebillingApp(None, root)
    app.run()
