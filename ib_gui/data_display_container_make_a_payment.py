#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox, StringVar
from .utils import tk_center
from InsuranceBilling import date_convert, InsuranceService


class DataDisplayContainerMakeAPaymentWidget(tk.Toplevel):
    def __init__(self, service: InsuranceService, master=None, **kw):
        super(DataDisplayContainerMakeAPaymentWidget,self).__init__(master,**kw)
        self.master = master
        self.c_service = service
        
        self.section_title = tk.Frame(self)
        self.section_title.configure(height=25, width=960)
        self.lb_title = tk.Label(self.section_title)
        self.lb_title.configure(
            font="{Verdana} 10 {bold}",
            text='Make a Payment')
        self.lb_title.place(x=15)
        self.section_title.pack(anchor="w", padx=10, pady=10, side="top")
        self.section_title.pack_propagate(0)
        
        self.line_selector = tk.LabelFrame(self)
        self.line_selector.configure(height=2, width=140)
        self.line_selector.place(x=15, y=35)
        
        self.form_frame = tk.Frame(self)
        self.form_frame.configure(height=200, width=200)
        self.frame_desc = tk.Frame(self.form_frame)
        self.frame_desc.configure(height=200, width=200)
        self.lb_description = tk.Label(self.frame_desc)
        self.lb_description.configure(
            font="{Verdana} 8 {}",
            text='Service description:',
            width=20)
        self.lb_description.pack(anchor="e", side="left")
        self.entry_description = tk.Entry(self.frame_desc)
        self.entry_description.configure(
            font="{Verdana} 9 {}",
            justify="left",
            state="disabled",
            width=50)
        self.entry_description.pack(ipady=5, side="top")
        self.frame_desc.pack(fill="x", side="top")
        self.frame_date = tk.Frame(self.form_frame)
        self.frame_date.configure(height=200, width=200)
        self.lb_date = tk.Label(self.frame_date)
        self.lb_date.configure(
            font="{Verdana} 8 {}",
            text='Service date:',
            width=20)
        self.lb_date.pack(anchor="e", side="left")
        self.entry_date = tk.Entry(self.frame_date)
        self.entry_date.configure(
            font="{Verdana} 9 {}",
            justify="left",
            state="disabled",
            width=50)
        self.entry_date.pack(ipady=5, side="top")
        self.frame_date.pack(fill="x", pady=20, side="top")
        self.frame_cost = tk.Frame(self.form_frame)
        self.frame_cost.configure(height=200, width=200)
        self.lb_cost = tk.Label(self.frame_cost)
        self.lb_cost.configure(
            font="{Verdana} 8 {}",
            text='Service cost:',
            width=20)
        self.lb_cost.pack(anchor="e", side="left")
        self.cost_frame = tk.Frame(self.frame_cost)
        self.cost_frame.configure(height=200, width=200)
        self.lb_dollar_sign = tk.Label(self.cost_frame)
        self.lb_dollar_sign.configure(font="{Verdana} 10 {}", text='$')
        self.lb_dollar_sign.pack(anchor="e", padx=5, side="left")
        self.entry_cost = tk.Entry(self.cost_frame)
        self.entry_cost.configure(
            font="{Verdana} 9 {}",
            justify="left",
            state="disabled",
            width=10)
        self.entry_cost.pack(ipady=5, side="bottom")
        self.cost_frame.pack(side="top")
        self.frame_cost.pack(fill="x", side="top")
        self.entry_frame = tk.Frame(self.form_frame)
        self.entry_frame.configure(height=200, width=200)
        self.lb_payamt = tk.Label(self.entry_frame)
        self.lb_payamt.configure(
            font="{Verdana} 8 {}",
            text='Payment amount:',
            width=20)
        self.lb_payamt.pack(anchor="e", side="left")
        self.payamt_frame = tk.Frame(self.entry_frame)
        self.payamt_frame.configure(height=200, width=200)
        self.lb_dollar_sign_2 = tk.Label(self.payamt_frame)
        self.lb_dollar_sign_2.configure(font="{Verdana} 10 {}", text='$')
        self.lb_dollar_sign_2.pack(anchor="e", padx=5, side="left")
        
        self.entry_cost_value = StringVar()
        self.entry_cost_value.trace_add("write", self.cost_entry_upd)
        self.entry_payment_amount = tk.Entry(self.payamt_frame, textvariable=self.entry_cost_value)
        self.entry_payment_amount.configure(
            font="{Verdana} 9 {}", justify="left", width=10)
        self.entry_payment_amount.pack(ipady=5, side="bottom")
        self.payamt_frame.pack(side="top")
        self.entry_frame.pack(fill="x", pady=20, side="top")
        self.form_frame.pack(
            anchor="w",
            fill="x",
            padx=15,
            pady=10,
            side="top")
        
        if service is not None:
            self.entry_description.configure(state=tk.NORMAL)
            self.entry_date.configure(state=tk.NORMAL)
            self.entry_cost.configure(state=tk.NORMAL)
            self.entry_description.insert(0, self.c_service.description)
            self.entry_date.insert(0, date_convert(_date=self.c_service.date))
            self.entry_cost.insert(0, self.c_service.cost[1:])
            self.entry_payment_amount.insert(0, self.c_service.amount_due[1:])
            self.entry_description.configure(state=tk.DISABLED)
            self.entry_date.configure(state=tk.DISABLED)
            self.entry_cost.configure(state=tk.DISABLED)
            
        self.control_container = tk.Frame(self)
        self.btn_pay = tk.Button(self.control_container)
        self.btn_pay.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            takefocus=True,
            text='Pay Now ✓')
        self.btn_pay.pack(ipadx=5, ipady=5, side="right")
        self.btn_pay.configure(command=self.form_submit)
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
        self.control_container.pack(anchor="e", padx=30, side="top")
        self.configure(takefocus=True, width=200)
        self.geometry("640x310")
        self.resizable(False, False)
        self.title("Make a Payment - Healthcare Permanente")
        
        self.lb_warning = tk.Label(self)
        self.lb_warning.configure(font="{Verdana} 8 {bold}", fg='#ffaa00')

        self.ddc = self.master.calls(widget_name="ddc")

        tk_center(self, gui_w=640, gui_h=320)
        self.focus_force()

    def form_submit(self):
        data = {'payment_amount': "$" + self.entry_payment_amount.get()}
        if not any(data.values()):
            messagebox.showwarning("Warning", "Make sure to fill out all fields before continue.")
        else:
            self.destroy()
            if data['payment_amount'] == "":
                self.ddc.toplevel_callback()
            else:
                self.ddc.toplevel_data_payment_callback(data)

    def form_cancel(self):
        if "" != self.entry_description.get() + self.entry_cost.get():
            if not messagebox.askyesno("Quit", f"You have not made a payment for this service yet. Are you sure you want to close this window?"):
                self.deiconify()
                return
        self.destroy()
        self.ddc.toplevel_callback()
        
    def cost_entry_upd(self, *event):
        value = self.entry_cost_value.get()
        if value in [".", ""]:
            return
        
        if hasattr(self, "lb_warning"):
            if not value.replace(" ", 'S').replace(".,", 'E').replace(",", "").replace(".", "", 1).isnumeric():
                x, y = self.payamt_frame.winfo_x(), self.payamt_frame.winfo_y()
                self.lb_warning.configure(text="Only digits (0-9) and ',.' are allowed here.")
                self.lb_warning.place(x=x*0.8, y=y+230)
                self.btn_pay.configure(state=tk.DISABLED)
            else:
                if "." in value:
                    if len(value[value.find(".")+1:]) > 2:
                        x, y = self.payamt_frame.winfo_x(), self.payamt_frame.winfo_y()
                        self.lb_warning.configure(text="Cent part should only have at most 2 digits.")
                        self.lb_warning.place(x=x*0.8, y=y+230)
                        self.btn_pay.configure(state=tk.DISABLED)
                        return
                self.lb_warning.place_forget()
                self.btn_pay.configure(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    widget = DataDisplayContainerMakeAPaymentWidget(root)
    # widget.pack(expand=True, fill="both")
    root.mainloop()
