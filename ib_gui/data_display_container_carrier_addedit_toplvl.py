#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from .utils import tk_center
from InsuranceBilling import InsuranceCarrier


class CarrierAddEditToplvlWidget(tk.Toplevel):
    def __init__(self, master=None, carrier: InsuranceCarrier=None, **kw):
        super(CarrierAddEditToplvlWidget, self).__init__(master, **kw)
        self.master = master
        self.c_carrier = carrier

        self.section_title = tk.Frame(self)
        self.section_title.configure(height=25, width=960)
        self.lb_title = tk.Label(self.section_title)
        self.lb_title.configure(font="{Verdana} 10 {bold}", text='Add/Edit Carrier')
        self.lb_title.place(x=15)
        self.section_title.pack(anchor="w", padx=10, pady=10, side="top")
        self.section_title.pack_propagate(0)
        self.line_selector = tk.LabelFrame(self)
        self.line_selector.configure(height=2, width=140)
        self.line_selector.place(x=15, y=35)

        self.form_frame = tk.Frame(self)
        self.form_frame.configure(height=200, width=200)
        self.lb_frame = tk.Frame(self.form_frame)
        self.lb_frame.configure(height=200, width=200)
        self.lb_name = tk.Label(self.lb_frame)
        self.lb_name.configure(font="{Verdana} 8 {}", text='Carrier name:', width=20)
        self.lb_name.pack(padx=10, side="top")
        self.lb_address = tk.Label(self.lb_frame)
        self.lb_address.configure(font="{Verdana} 8 {}", text='Carrier address:', width=20)
        self.lb_address.pack(padx=10, pady=30, side="top")
        self.lb_primary = tk.Label(self.lb_frame)
        self.lb_primary.configure(font="{Verdana} 8 {}", text='Is this a primary carrier?', width=20)
        self.lb_primary.pack(padx=10, side="top")
        self.lb_frame.pack(side="left")
        
        self.entry_frame = tk.Frame(self.form_frame)
        self.entry_frame.configure(height=200, width=200)
        self.entry_name = tk.Entry(self.entry_frame)
        self.entry_name.configure(font="{Verdana} 9 {}", justify="left", width=50)
        self.entry_name.pack(ipady=5, side="top")
        self.entry_address = tk.Entry(self.entry_frame)
        self.entry_address.configure(font="{Verdana} 9 {}", justify="left", width=50)
        self.entry_address.pack(ipady=5, pady=20, side="top")
        self.entry_primary = ttk.Combobox(self.entry_frame)
        self.entry_primary.configure(justify="center", state="readonly", values="PRIMARY NON-PRIMARY")
        self.entry_primary.current(1)
        self.entry_primary.pack(side="top")
        self.entry_primary.bind("<<ComboboxSelected>>", self.primary_entry_upd)
        
        if carrier is not None:
            self.entry_name.delete(0, tk.END)
            self.entry_address.delete(0, tk.END)
            self.entry_primary.delete(0, tk.END)
            self.entry_name.insert(0, self.c_carrier.name)
            self.entry_address.insert(0, self.c_carrier.address)
            self.entry_primary.current(0 if self.c_carrier.primary else 1)
            
        self.entry_frame.pack(padx=20, side="right")
        self.form_frame.pack(anchor="w", padx=15, pady=10, side="top")

        self.control_container = tk.Frame(self)
        self.btn_done = tk.Button(self.control_container)
        self.btn_done.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            takefocus=True,
            text='Done ✓')
        self.btn_done.pack(ipadx=5, ipady=5, side="right")
        self.btn_done.configure(command=self.form_submit)
        self.btn_cancel = tk.Button(self.control_container)
        self.btn_cancel.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            text='× Cancel')
        self.btn_cancel.pack(ipadx=5, ipady=5, padx=10, side="right")
        self.btn_cancel.configure(command=self.form_cancel)
        self.control_container.pack(padx=30, pady=20, side="bottom", fill="x")
        
        self.geometry("640x270")
        self.resizable(False, False)
        self.title("Adding new carrier - Healthcare Permanente")
        self.protocol("WM_DELETE_WINDOW", self.form_cancel)

        self.lb_warning = tk.Label(self)
        self.lb_warning.configure(font="{Verdana} 8 {bold}", fg='#ffaa00')


        self.ddc = self.master.calls(widget_name="ddc")
        
        tk_center(self, gui_w=640, gui_h=270)
        self.focus_force()

    def primary_entry_upd(self, event=None):
        if not self.c_carrier.primary and self.entry_primary.get() == "PRIMARY":
            x, y = event.widget.winfo_x(), event.widget.winfo_y()
            self.lb_warning.configure(text="Warning: by setting this to PRIMARY will modify all other\ncarriers primary status to NON-PRIMARY.")
            self.lb_warning.place(x=x*1.7, y=y+80)
        elif self.c_carrier.primary and self.entry_primary.get() == "NON-PRIMARY":
            x, y = event.widget.winfo_x(), event.widget.winfo_y()
            self.lb_warning.configure(text="Warning: by setting this to NON-PRIMARY will assign the most\nrecent carrier primary status to PRIMARY.")
            self.lb_warning.place(x=x*1.5, y=y+80)
        else:
            self.lb_warning.place_forget()

    def form_submit(self):
        data = {'name': self.entry_name.get(),
                'address': self.entry_address.get(),
                'primary': self.entry_primary.get()}
        
        if not any(data.values()):
            messagebox.showwarning("Warning", "Make sure to fill out all fields before continue.")
        else:
            self.destroy()
            if data['primary'] == "NON-PRIMARY" and "" == data['address'] + data['name']: 
                self.ddc.toplevel_callback()
            else:
                if self.c_carrier is not None:
                    self.ddc.toplevel_data_edit_callback(data)
                else:
                    self.ddc.toplevel_data_transfer_callback(data)

    def form_cancel(self):
        if "" != self.entry_name.get() + self.entry_address.get():
            if not messagebox.askyesno("Quit", "You have unsaved changes. Are you sure you want to close this window?"):
                self.deiconify()
                return
        self.destroy()
        self.ddc.toplevel_callback()


if __name__ == "__main__":
    root = tk.Tk()
    widget = CarrierAddEditToplvlWidget(root)
    # widget.pack(expand=True, fill="both")
    widget.mainloop()
