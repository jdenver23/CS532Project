#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from .utils import tk_center
from InsuranceBilling import InsuranceBilling, InsuranceInvoice, dollar_to_float


class InvoiceViewWidget(tk.Toplevel):
    def __init__(self, master=None, invoice: InsuranceInvoice=None, bill: InsuranceBilling=None, **kw):
        super(InvoiceViewWidget,self).__init__(master,**kw)
        self.master = master
        self.bill = bill
        self.c_invoice = invoice
        
        self.section_title = tk.Frame(self)
        self.section_title.configure(height=25, width=960)
        self.lb_title = tk.Label(self.section_title)
        self.lb_title.configure(
            font="{Verdana} 10 {bold}",
            text='Invoice Infomation')
        self.lb_title.place(x=15)
        self.section_title.pack(anchor="w", padx=10, pady=10, side="top")
        self.section_title.pack_propagate(0)
        self.line_selector = tk.LabelFrame(self)
        self.line_selector.configure(height=2, width=165)
        self.line_selector.place(x=15, y=35)
        
        self.invoice_select = tk.Frame(self)
        self.invoice_select.configure(height=25, width=960)
        self.lb_invoice_select = tk.Label(self.invoice_select)
        self.lb_invoice_select.configure(
            font="{Verdana} 10 {}", text='Select invoice:')
        self.lb_invoice_select.pack(padx=25, side="left")
        
        self.entry_invoice_sel = ttk.Combobox(self.invoice_select)
        self.entry_invoice_sel.configure(state="readonly")
        self.entry_invoice_sel.pack(anchor="w", fill="x", ipady=15, padx=15, side="top")
        self.all_invoices_info = [f"[ID: {str(inv.id)}] " +
                                  f"AMOUNT {dollar_to_float(inv.amount_due)}/{dollar_to_float(inv.total_cost)} " + 
                                  f"@ {inv.carrier_info[0]} ({inv.status.name})" for inv in self.bill.invoices]
        self.entry_invoice_sel.configure(state="readonly", values=self.all_invoices_info)
        for invoice_info in self.all_invoices_info:
            if self.invoice_info_to_id(invoice_info) == str(self.c_invoice.id):
                self.entry_invoice_sel.set(invoice_info)
                break
        self.entry_invoice_sel.bind("<<ComboboxSelected>>", self.entry_invoice_sel_upd)
        
        self.invoice_select.pack(anchor="w", padx=10, side="top")
        self.invoice_select.pack_propagate(0)
        
        self.frame_invoice_info = tk.Frame(self)
        self.text_invoice_info = ScrolledText(self.frame_invoice_info, font="{Verdana} 10 {}", height=20)    
        self.text_invoice_info.configure(state=tk.DISABLED)    
        self.text_invoice_info.pack(padx=15, pady=20, ipadx=5, fill="both", side="top", expand=True)
        self.frame_invoice_info.pack(fill="x", side="top")
        self.entry_invoice_sel_upd()
        
        self.control_container = tk.Frame(self)
        self.btn_back = tk.Button(self.control_container)
        self.btn_back.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            overrelief="ridge",
            relief="flat",
            text='⬅ Back')
        self.btn_back.pack(ipadx=10, side="top")
        self.btn_back.configure(command=self.form_cancel)
        self.control_container.pack(anchor="w", padx=15, side="top")
        
        self.protocol("WM_DELETE_WINDOW", self.form_cancel)
        self.configure(takefocus=True)
        self.geometry("720x490")
        self.resizable(False, False)
        self.title("Invoice Information - Healthcare Permanente")
        self.focus_force()
        
        self.ddc = self.master.calls(widget_name="ddc")
        
        tk_center(self, gui_w=720, gui_h=490)
        self.focus_force()

    def invoice_info_to_id(self, info: str):
        return info.split("]")[0].replace("[ID: ", "")
    
    def entry_invoice_sel_upd(self, event=None):
        _id_ = self.invoice_info_to_id(self.entry_invoice_sel.get())
        _info = self.bill.invoice_info(_id_)
        if _info != "":
            self.text_invoice_info.configure(state=tk.NORMAL)
            self.text_invoice_info.delete("0.0", tk.END)
            self.text_invoice_info.insert(tk.END, _info)
            self.text_invoice_info.configure(state=tk.DISABLED)
        
    def form_cancel(self):
        self.destroy()
        self.ddc.toplevel_callback()


if __name__ == "__main__":
    root = tk.Tk()
    widget = InvoiceViewWidget(root)
    # widget.pack(expand=True, fill="both")
    root.mainloop()
