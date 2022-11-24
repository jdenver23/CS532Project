#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, StringVar
from .utils import tk_center
from InsuranceBilling import InsuranceInvoice, InsuranceBilling, date_convert, dollar_to_float


class DataDisplayContainerMakeAPaymentWidget(tk.Toplevel):
    def __init__(self, invoice: InsuranceInvoice, bill: InsuranceBilling, master=None, **kw):
        super(DataDisplayContainerMakeAPaymentWidget,self).__init__(master,**kw)
        self.master = master
        self.c_invoice = invoice
        self.bill = bill
        
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
        self.invoice_select = tk.Frame(self)
        self.invoice_select.configure(height=25, width=960)
        self.lb_invoice_select = tk.Label(self.invoice_select)
        self.lb_invoice_select.configure(font="{Verdana} 10 {}", text='Select invoice:')
        self.lb_invoice_select.pack(padx=25, side="left")
        
        self.entry_invoice_sel = ttk.Combobox(self.invoice_select)
        self.all_invoices_info = [f"[ID: {str(inv.id)}] " +
                                  f"AMOUNT {dollar_to_float(inv.amount_due)}/{dollar_to_float(inv.total_cost)} " + 
                                  f"@ {inv.carrier_info[0]} ({inv.status.name})" for inv in self.bill.invoices]
        self.entry_invoice_sel.configure(state="readonly", values=self.all_invoices_info)
        for invoice_info in self.all_invoices_info:
            if self.invoice_info_to_id(invoice_info) == str(self.c_invoice.id):
                self.entry_invoice_sel.set(invoice_info)
                break
        self.entry_invoice_sel.pack(anchor="w", padx=15, ipady=15, side="top", fill="x")
        self.entry_invoice_sel.bind("<<ComboboxSelected>>", self.entry_invoice_sel_upd)
        
        self.invoice_select.pack(anchor="w", padx=10, side="top")
        self.invoice_select.pack_propagate(0)
        
        self.treeview_fr = tk.Frame(self)
        self.left_pad = tk.Label(self.treeview_fr)
        self.left_pad.configure(justify="left")
        self.left_pad.pack(anchor="w", side="left")
        self.right_pad = tk.Label(self.treeview_fr)
        self.right_pad.configure(justify="left")
        self.right_pad.pack(anchor="e", side="right")
        self.treeview_services = ttk.Treeview(self.treeview_fr)
        self.create_services_tv(self.treeview_fr)
        self.fill_in_services(from_invoice=self.c_invoice)
        self.treeview_fr.pack(anchor="n", fill="x", padx=10, pady=10, side="top")
        
        self.frame_service = tk.Frame(self)
        self.frame_service.configure(height=200, width=200)
        self.form_frame = tk.Frame(self.frame_service)
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
        self.lb_dollar_sign_2.pack(anchor="w", padx=5, side="left")
        
        self.entry_payment_amount_value = StringVar()
        self.entry_payment_amount_value.trace_add("write", self.cost_entry_upd)
        self.entry_payment_amount = tk.Entry(self.payamt_frame, textvariable=self.entry_payment_amount_value)
        self.entry_payment_amount.configure(
            font="{Verdana} 9 {}", justify="left", width=10)
        self.entry_payment_amount.pack(ipady=5, side="left")
        self.lb_amount_due = tk.Label(self.payamt_frame)
        self.lb_amount_due.configure(font="{Verdana} 10 {}", text=f'/ {self.c_invoice.amount_due}')
        self.lb_amount_due.pack(anchor="e", padx=5, side="left")
        self.payamt_frame.pack(side="top")
        self.entry_frame.pack(fill="x", pady=20, side="top")
        self.form_frame.pack(anchor="w", fill="x", padx=15, side="top")
        self.frame_service.pack(fill="x", side="top")
        
        self.control_container = tk.Frame(self.frame_service)
        self.btn_pay = tk.Button(self.control_container)
        self.btn_pay.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            takefocus=True,
            overrelief="ridge",
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
            overrelief="ridge",
            text='× Cancel')
        self.btn_cancel.pack(ipadx=5, ipady=5, padx=10, side="right")
        self.btn_cancel.configure(command=self.form_cancel)
        self.control_container.pack(fill="x", padx=30, side="top")
        self.configure(takefocus=True, width=200)
        self.geometry("720x470")
        self.resizable(False, False)
        self.title("Make a Payment - Healthcare Permanente")
        self.protocol("WM_DELETE_WINDOW", self.form_cancel)
        
        self.lb_warning = tk.Label(self)
        self.lb_warning.configure(font="{Verdana} 8 {bold}", fg='#ffaa00')

        self.ddc = self.master.calls(widget_name="ddc")
        
        tk_center(self, gui_w=720, gui_h=470)
        self.focus_force()
        
    def cost_entry_upd(self, *event):
        value = self.entry_payment_amount_value.get()
        if value in [".", ""]:
            return
        
        if hasattr(self, "lb_warning"):
            if not value.replace(" ", 'S').replace(".,", 'E').replace(",", "").replace(".", "", 1).isnumeric():
                x, y = self.payamt_frame.winfo_x(), self.payamt_frame.winfo_y()
                self.lb_warning.configure(text="Only digits (0-9) and ',.' are allowed here.")
                self.lb_warning.place(x=x*0.85, y=y+400)
                self.btn_pay.configure(state=tk.DISABLED)
            else:
                if "." in value:
                    if len(value[value.find(".")+1:]) > 2:
                        x, y = self.payamt_frame.winfo_x(), self.payamt_frame.winfo_y()
                        self.lb_warning.configure(text="Cent part should only have at most 2 digits.")
                        self.lb_warning.place(x=x*0.8, y=y+400)
                        self.btn_pay.configure(state=tk.DISABLED)
                        return
                self.lb_warning.place_forget()
                self.btn_pay.configure(state=tk.NORMAL)
    
    def invoice_info_to_id(self, info: str):
        return info.split("]")[0].replace("[ID: ", "")
    
    def entry_invoice_sel_upd(self, event=None):
        _id_ = self.invoice_info_to_id(self.entry_invoice_sel.get())
        self.fill_in_services(from_invoice=self.bill.get_invoice(_id_))
    
    def treeview_click_handler(self, event):
        # disable column resizing by disable mouse click at "separator"
        if event.widget.identify_region(event.x, event.y) == "separator":
            return "break"
        
        self.selected_item_id = event.widget.identify('item', event.x, event.y)
        self.selected_row = event.widget.item(self.selected_item_id)['values']
        if self.selected_item_id != "":
            selected_service = self.c_invoice.get_service(self.selected_row[0])
            if selected_service is not None:
                self.entry_description.configure(state=tk.NORMAL)
                self.entry_date.configure(state=tk.NORMAL)
                self.entry_cost.configure(state=tk.NORMAL)
                self.entry_description.delete(0, tk.END)
                self.entry_date.delete(0, tk.END)
                self.entry_cost.delete(0, tk.END)
                self.entry_description.insert(0, selected_service.description)
                self.entry_date.insert(0, date_convert(_date=selected_service.date))
                self.entry_cost.insert(0, selected_service.cost[1:])
                self.entry_description.configure(state=tk.DISABLED)
                self.entry_date.configure(state=tk.DISABLED)
                self.entry_cost.configure(state=tk.DISABLED)
        else:
            pass
        
    def create_services_tv(self, root):
        self.service_columns = ('id', 'description', 'date', 'cost', 'payment_status')
        self.treeview_services = ttk.Treeview(root)
        self.treeview_services.configure(height=3, selectmode="extended", show="headings", columns=self.service_columns)
        self.treeview_services.bind("<Button-1>", self.treeview_click_handler)

        self.treeview_services.heading('id', text="ID", command=lambda: self.treeview_sort_column(self.treeview_services, 'id'))
        self.treeview_services.column('id', anchor=tk.CENTER, width=50)
        self.treeview_services.heading('description', text="Description", command=lambda: self.treeview_sort_column(self.treeview_services, 'description'))
        self.treeview_services.column('description', anchor=tk.CENTER, width=330)
        self.treeview_services.heading('date', text="Date", command=lambda: self.treeview_sort_column(self.treeview_services, 'date'))
        self.treeview_services.column('date', anchor=tk.CENTER, width=105)
        self.treeview_services.heading('cost', text="Cost", command=lambda: self.treeview_sort_column(self.treeview_services, 'cost'))
        self.treeview_services.column('cost', anchor=tk.CENTER, width=105)
        self.treeview_services.heading('payment_status', text="Status", command=lambda: self.treeview_sort_column(self.treeview_services, 'payment_status'))
        self.treeview_services.column('payment_status', anchor=tk.CENTER, width=70)
        self.treeview_services.pack(expand="true", fill="x", padx=10, pady=10, side="top")

    def treeview_sort_column(self, treeview, col, reverse=True):
        """Sort treeview column by name."""
        l = [(treeview.set(k, col), k) for k in treeview.get_children('')]
        l.sort(key=lambda x: dollar_to_float(x[0]) if col == 'cost' else x, reverse=reverse)

        for index, (val, k) in enumerate(l):
            treeview.move(k, '', index)

        treeview.heading(col, command=lambda: self.treeview_sort_column(treeview, col, not reverse))

    def treeview_forced_set_state(self, treeview: ttk.Treeview, show=False):
        if not show:
            treeview.pack_forget()
        else:
            treeview.pack(expand="true", fill="x",padx=10, pady=10, side="top")

    def treeview_insert_row(self, treeview: ttk.Treeview, list_rows: list(list())):
        for row in list_rows:
            treeview.insert("", tk.END, values=row)
            
    def fill_in_services(self, from_invoice: InsuranceInvoice):
        self.treeview_services.delete(*self.treeview_services.get_children())
        self.treeview_insert_row(self.treeview_services, [service.as_list() for service in from_invoice.invoiced_services])
        self.c_invoice = from_invoice
        if hasattr(self, "lb_amount_due"): 
            self.lb_amount_due.configure(text=f"/ {from_invoice.amount_due}")
            self.entry_description.configure(state=tk.NORMAL)
            self.entry_date.configure(state=tk.NORMAL)
            self.entry_cost.configure(state=tk.NORMAL)
            self.entry_description.delete(0, tk.END)
            self.entry_date.delete(0, tk.END)
            self.entry_cost.delete(0, tk.END)
            self.entry_description.configure(state=tk.DISABLED)
            self.entry_date.configure(state=tk.DISABLED)
            self.entry_cost.configure(state=tk.DISABLED)

    def form_submit(self):
        data = {'payment_amount': self.entry_payment_amount.get()}
        if any(not val for val in data.values()):
            messagebox.showwarning("Warning", "Make sure to fill out all fields before continue.")
            self.focus_force()
        else:
            data["payment_amount"] = "$" + data["payment_amount"]
            self.destroy()
            if data['payment_amount'] == "":
                self.ddc.toplevel_callback()
            else:
                self.ddc.toplevel_data_payment_callback(data)

    def form_cancel(self):
        if "" != self.entry_cost.get():
            if not messagebox.askyesno("Quit", f"You have not made a payment for this service yet. Are you sure you want to close this window?"):
                self.focus_force()
                return
        self.destroy()
        self.ddc.toplevel_callback()


if __name__ == "__main__":
    root = tk.Tk()
    widget = DataDisplayContainerMakeAPaymentWidget(root)
    # widget.pack(expand=True, fill="both")
    root.mainloop()
