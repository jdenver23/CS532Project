#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from .data_display_container_make_a_payment import DataDisplayContainerMakeAPaymentWidget
from .data_display_container_invoice_view import InvoiceViewWidget
from InsuranceBilling import InsuranceBilling, dollar_to_float


class DataDisplayContainerUserWidget(tk.Frame):
    def __init__(self, bill: InsuranceBilling, master=None, test_data=False, **kw):
        super(DataDisplayContainerUserWidget, self).__init__(master, **kw)
        self.bill = bill

        self.section_title = tk.Frame(self)
        self.section_title.configure(height=25, width=960)
        self.title_carriers = tk.Label(self.section_title)
        self.title_carriers.configure(font="{Verdana} 10 {bold}", text='Carriers')
        self.title_carriers.place(x=15)
        self.title_services = tk.Label(self.section_title)
        self.title_services.configure(font="{Verdana} 10 {}", text='Services')
        self.title_services.place(x=95, y=0)
        self.title_invoices = tk.Label(self.section_title)
        self.title_invoices.configure(font="{Verdana} 10 {}", text='Invoices')
        self.title_invoices.place(x=175, y=0)
        self.section_title.pack(anchor="w", padx=10, pady=10, side="top")
        self.section_title.pack_propagate(0)

        self.title_carriers.bind("<Button-1>", self.toggle_treeview)
        self.title_services.bind("<Button-1>", self.toggle_treeview)
        self.title_invoices.bind("<Button-1>", self.toggle_treeview)

        self.line_selector = tk.LabelFrame(self)
        self.line_selector.configure(height=2, width=40)
        self.line_selector.place(x=40, y=35)

        self.treeview_fr = tk.Frame(self)

        self.left_pad = tk.Label(self.treeview_fr)
        self.left_pad.configure(justify="left")
        self.left_pad.pack(anchor="w", side="left")
        self.right_pad = tk.Label(self.treeview_fr)
        self.right_pad.configure(justify="left")
        self.right_pad.pack(anchor="e", side="right")

        self.selected_row = ""
        self.create_carriers_tv(self.treeview_fr)
        self.create_services_tv(self.treeview_fr)
        self.create_invoices_tv(self.treeview_fr)
        self.treeview_forced_set_state(self.treeview_carriers, show=True)
        self.treeview_reset_sel()
        self.active_treeview = "Carriers"
        
        if test_data:
            self.add_test_data()

        treeview_style = ttk.Style()
        treeview_style.configure("Treeview.Heading", font="{Verdana} 10 {}")
        treeview_style.configure('Treeview', rowheight=25)

        self.treeview_fr.pack(anchor="n", padx=10, pady=10, side="top")

        self.control_container = tk.Frame(self)
        
        self.btn_view = tk.Button(self.control_container)
        self.btn_view.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            state="disabled",
            overrelief="ridge",
            text='ⓘ View')
        self.btn_view.configure(command=lambda: self.treeview_view_selection())
        self.btn_pay = tk.Button(self.control_container)
        self.btn_pay.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            state="disabled",
            takefocus=True,
            overrelief="ridge",
            text="Make a Payment")
        self.btn_pay.configure(command=lambda: self.selection_pay())

        self.control_container.pack(anchor="n", padx=30, side="top", fill="x")

        self.configure(height=550, width=960)
        self.pack_propagate(0)

        # hotkeys:
        # "a" or "d" to move tab left/right
        # "w" or "s" to select item
        self.master.bind("d", lambda x: self.toggle_treeview_tab(direction="right"))
        self.master.bind("a", lambda x: self.toggle_treeview_tab(direction="left"))
        self.master.bind("w", lambda x: self.toggle_treeview_item(direction="up"))
        self.master.bind("s", lambda x: self.toggle_treeview_item(direction="down"))
        
        self.pull_from_db()
    
    def selection_pay(self):
        self.master.attributes("-disabled", True)
        self.toplevel_force_focus_fid = self.master.bind("<Button-1>", self.toplevel_force_focus)
        
        if self.active_treeview == "Invoices":
            self.curr_selected = self.treeview_invoices.selection()[0]
            self.id_to_edit = self.treeview_invoices.item(self.curr_selected)['values'][0]
            self.curr_toplvl = DataDisplayContainerMakeAPaymentWidget(invoice=self.bill.get_invoice(self.id_to_edit), 
                                                                      bill=self.bill,
                                                                      master=self.master)
        else:
            self.reset_attributes()
        

    def pull_from_db(self, refresh=True, renew_carriers=True, renew_services=True, renew_invoices=True):
        self.btn_pay.configure(state=tk.DISABLED)
        
        # remove all children from all treeviews
        if renew_carriers: self.treeview_carriers.delete(*self.treeview_carriers.get_children())
        if renew_services: self.treeview_services.delete(*self.treeview_services.get_children())
        if renew_invoices: self.treeview_invoices.delete(*self.treeview_invoices.get_children())

        # reset local lists from database data
        if refresh:
            self.bill.retrieve_data()

        # get data from db then insert to treeviews
        if renew_carriers: self.treeview_insert_row(self.treeview_carriers, [carrier.as_list() for carrier in self.bill.carriers])
        if renew_services: self.treeview_insert_row(self.treeview_services, [service.as_list() for service in self.bill.services])
        if renew_invoices: self.treeview_insert_row(self.treeview_invoices, [invoice.as_list() for invoice in self.bill.invoices])
            
    def reset_attributes(self):
        """Focus on master and permit mouse clicking."""
        self.master.unbind("<Button-1>", self.toplevel_force_focus_fid)
        self.master.focus_force()
        self.master.attributes("-disabled", False)
    
    def treeview_view_selection(self) -> None:
        self.master.attributes("-disabled", True)
        self.toplevel_force_focus_fid = self.master.bind("<Button-1>", self.toplevel_force_focus)
        
        if self.active_treeview == "Invoices":
            self.curr_selected = self.treeview_invoices.selection()[0]
            self.id_to_edit = self.treeview_invoices.item(self.curr_selected)['values'][0]
            self.curr_toplvl = InvoiceViewWidget(master=self.master, invoice=self.bill.get_invoice(self.id_to_edit), bill=self.bill)
    
    def treeview_reset_sel(self):
        self.treeview_carriers_curr_sel = None
        self.treeview_services_curr_sel = None
        self.treeview_invoices_curr_sel = None
        
    def toggle_treeview_item(self, direction="down", event=None):
        dx = -1 if direction == "up" else 1
        
        if self.active_treeview == "Carriers":
            if self.treeview_carriers_curr_sel is None: self.treeview_carriers_curr_sel = 0 if dx == 1 else -1
            else: self.treeview_carriers_curr_sel += dx
            all_child = self.treeview_carriers.get_children()
            if self.treeview_carriers_curr_sel >= len(all_child):
                self.treeview_carriers_curr_sel = 0
            elif self.treeview_carriers_curr_sel < 0: 
                self.treeview_carriers_curr_sel = len(all_child)-1
            self.selected_item_id = all_child[self.treeview_carriers_curr_sel]
            self.treeview_carriers.selection_set(self.selected_item_id)
            self.treeview_sel_handler()
        elif self.active_treeview == "Services":
            if self.treeview_services_curr_sel is None: self.treeview_services_curr_sel = 0 if dx == 1 else -1
            else: self.treeview_services_curr_sel += dx
            all_child = self.treeview_services.get_children()
            if self.treeview_services_curr_sel >= len(all_child):
                self.treeview_services_curr_sel = 0
            elif self.treeview_services_curr_sel < 0: 
                self.treeview_services_curr_sel = len(all_child)-1
            self.selected_item_id = all_child[self.treeview_services_curr_sel]
            self.treeview_services.selection_set(self.selected_item_id)
            self.treeview_sel_handler()
        elif self.active_treeview == "Invoices":
            if self.treeview_invoices_curr_sel is None: self.treeview_invoices_curr_sel = 0 if dx == 1 else -1
            else: self.treeview_invoices_curr_sel += dx
            all_child = self.treeview_invoices.get_children()
            if self.treeview_invoices_curr_sel >= len(all_child):
                self.treeview_invoices_curr_sel = 0
            elif self.treeview_invoices_curr_sel < 0: 
                self.treeview_invoices_curr_sel = len(all_child)-1
            self.selected_item_id = all_child[self.treeview_invoices_curr_sel]
            self.treeview_invoices.selection_set(self.selected_item_id)
            self.treeview_sel_handler()
        
    def toggle_treeview_tab(self, direction="right", event=None):
        idx = 1 if direction == "right" else 2
        if self.active_treeview == "Services":
            idx = 2 if direction == "right" else 0
        elif self.active_treeview == "Invoices":
            idx = 0 if direction == "right" else 1
        self.treeview_reset_sel()
        self.toggle_treeview(index=idx)

    def toplevel_callback(self, event=None):
        """`DDC` default call back."""
        self.reset_attributes()

    def toplevel_data_commit_callback(self):
        """`DDC` commit data call back."""
        self.reset_attributes()
        self.bill.commit_to_db()
    
    def toplevel_data_payment_callback(self, data: dict):
        """`DDC` payment call back."""
        self.reset_attributes()
        
        if any(data.values()) and hasattr(self, "id_to_edit"):
            if self.active_treeview == "Invoices":
                self.bill.pay_for_invoice(invoice_id=self.id_to_edit, payment_amount=data['payment_amount'])
                self.treeview_invoices.item(self.curr_selected, values=self.bill.get_invoice(self.id_to_edit).as_list())
                self.bill.commit_to_db()
                self.pull_from_db(refresh=True)
    
    def toplevel_force_focus(self, event=None):
        if hasattr(self, "curr_toplvl"):
            self.curr_toplvl.focus_force()
            return "break"

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
            treeview.pack(expand="true", fill="x",
                          padx=10, pady=10, side="top")

    def treeview_insert_row(self, treeview: ttk.Treeview, list_rows: list(list())):
        for row in list_rows:
            treeview.insert("", tk.END, values=row)

    def treeview_click_handler(self, event):
        # disable column resizing by disable mouse click at "separator"
        if event.widget.identify_region(event.x, event.y) == "separator":
            return "break"
        
        # `btn_pay` custom behaviour
        self.selected_item_id = event.widget.identify('item', event.x, event.y)
        self.selected_row = event.widget.item(self.selected_item_id)['values']
        if event.widget.exists(self.selected_item_id):
            self.treeview_sel_handler()
        else:
            self.treeview_carriers.selection_remove(*self.treeview_carriers.selection())
            self.treeview_services.selection_remove(*self.treeview_services.selection())
            self.treeview_invoices.selection_remove(*self.treeview_invoices.selection())
    
    def treeview_sel_handler(self):
        if self.active_treeview == "Invoices" and self.selected_item_id != "":
            self.btn_view.configure(state=tk.NORMAL)
            payment_status = self.treeview_invoices.item(self.selected_item_id)['values'][6]
            if payment_status != "PAID":
                self.btn_pay.configure(state=tk.NORMAL)
            else:
                self.btn_pay.configure(state=tk.DISABLED)
        else:
            self.btn_pay.configure(state=tk.DISABLED)
            self.btn_view.configure(state=tk.DISABLED)

    def add_test_data(self):
        self.treeview_insert_row(self.treeview_carriers, [['2', 'a', '789', 'NON-PRIMARY'],
                                                          ['0', 'c', '123', 'PRIMARY'],
                                                          ['3', 'b', 'Street', 'NON-PRIMARY'],
                                                          ['1', 'd', '456', 'NON-PRIMARY'], ])
        self.treeview_insert_row(self.treeview_services, [['4', 'e', 'FDSF', '$12'],
                                                          ['5', 'f', 'jd5r', '$888'],
                                                          ['6', 'g', 'io', '$1'],
                                                          ['7', 'h', '#$456', '$65'], ])
        self.treeview_insert_row(self.treeview_invoices, [
                                 ['0', '1-1-2001', '2-1-2001', '$1200', 'test carrier', 'UNPAID', '', '123'], ])

    def toggle_treeview(self, event: tk.Event = None, index=None):
        """ Switch treeview on selected. """
        if index == 0 or (event is not None and event.widget.cget("text") == "Carriers"):
            self.active_treeview = "Carriers"
            self.treeview_carriers.selection_remove(*self.treeview_carriers.selection())
            self.treeview_services.selection_remove(*self.treeview_services.selection())
            self.treeview_invoices.selection_remove(*self.treeview_invoices.selection())
            self.title_carriers.config(font="{Verdana} 10 {bold}")
            self.title_services.config(font="{Verdana} 10 {}")
            self.title_invoices.config(font="{Verdana} 10 {}")
            self.treeview_forced_set_state(self.treeview_carriers, show=True)
            self.treeview_forced_set_state(self.treeview_services, show=False)
            self.treeview_forced_set_state(self.treeview_invoices, show=False)
            self.line_selector.place(x=40, y=35)
            self.title_services.place(x=95, y=0)
            self.btn_pay.pack_forget()
            self.btn_view.pack_forget()
        elif index == 1 or (event is not None and event.widget.cget("text") == "Services"):
            self.active_treeview = "Services"
            self.treeview_carriers.selection_remove(*self.treeview_carriers.selection())
            self.treeview_services.selection_remove(*self.treeview_services.selection())
            self.treeview_invoices.selection_remove(*self.treeview_invoices.selection())
            self.title_carriers.config(font="{Verdana} 10 {}")
            self.title_services.config(font="{Verdana} 10 {bold}")
            self.title_invoices.config(font="{Verdana} 10 {}")
            self.treeview_forced_set_state(self.treeview_carriers, show=False)
            self.treeview_forced_set_state(self.treeview_services, show=True)
            self.treeview_forced_set_state(self.treeview_invoices, show=False)
            self.line_selector.place(x=119, y=35)
            self.title_services.place(x=93, y=0)
            self.btn_pay.pack_forget()
            self.btn_view.pack_forget()
        elif index == 2 or (event is not None and event.widget.cget("text") == "Invoices"):
            self.active_treeview = "Invoices"
            self.treeview_carriers.selection_remove(*self.treeview_carriers.selection())
            self.treeview_services.selection_remove(*self.treeview_services.selection())
            self.treeview_invoices.selection_remove(*self.treeview_invoices.selection())
            self.title_carriers.config(font="{Verdana} 10 {}")
            self.title_services.config(font="{Verdana} 10 {}")
            self.title_invoices.config(font="{Verdana} 10 {bold}")
            self.treeview_forced_set_state(self.treeview_carriers, show=False)
            self.treeview_forced_set_state(self.treeview_services, show=False)
            self.treeview_forced_set_state(self.treeview_invoices, show=True)
            self.line_selector.place(x=202, y=35)
            self.title_services.place(x=95, y=0)
            self.btn_pay.pack(ipadx=5, ipady=5, side="right")
            self.btn_view.pack(ipadx=5, ipady=5, side="left")

        self.selected_item_id = ""
        self.selected_row = ""
        self.btn_pay.configure(state=tk.DISABLED)

    def create_carriers_tv(self, root):
        """ Initialize carriers treeview. """
        self.carrier_columns = ('id', 'name', 'address', 'primary')
        self.treeview_carriers = ttk.Treeview(root)
        self.treeview_carriers.configure(height=14, selectmode="extended", show="headings", columns=self.carrier_columns)
        self.treeview_carriers.bind("<Button-1>", self.treeview_click_handler)

        self.treeview_carriers.heading('id', text="ID", command=lambda: self.treeview_sort_column(self.treeview_carriers, 'id'))
        self.treeview_carriers.column('id', anchor=tk.CENTER, width=50)
        self.treeview_carriers.heading('name', text="Name", command=lambda: self.treeview_sort_column(self.treeview_carriers, 'name'))
        self.treeview_carriers.column('name', anchor=tk.CENTER, width=400)
        self.treeview_carriers.heading('address', text="Address", command=lambda: self.treeview_sort_column(self.treeview_carriers, 'address'))
        self.treeview_carriers.column('address', anchor=tk.CENTER, width=305)
        self.treeview_carriers.heading('primary', text="Primary", command=lambda: self.treeview_sort_column(self.treeview_carriers, 'primary'))
        self.treeview_carriers.column('primary', anchor=tk.CENTER, width=145)

    def create_services_tv(self, root):
        self.service_columns = ('id', 'description', 'date', 'cost', 'payment_status')
        self.treeview_services = ttk.Treeview(root)
        self.treeview_services.configure(height=14, selectmode="extended", show="headings", columns=self.service_columns)
        self.treeview_services.bind("<Button-1>", self.treeview_click_handler)

        self.treeview_services.heading('id', text="ID", command=lambda: self.treeview_sort_column(self.treeview_services, 'id'))
        self.treeview_services.column('id', anchor=tk.CENTER, width=50)
        self.treeview_services.heading('description', text="Description", command=lambda: self.treeview_sort_column(self.treeview_services, 'description'))
        self.treeview_services.column('description', anchor=tk.CENTER, width=440)
        self.treeview_services.heading('date', text="Date", command=lambda: self.treeview_sort_column(self.treeview_services, 'date'))
        self.treeview_services.column('date', anchor=tk.CENTER, width=135)
        self.treeview_services.heading('cost', text="Cost", command=lambda: self.treeview_sort_column(self.treeview_services, 'cost'))
        self.treeview_services.column('cost', anchor=tk.CENTER, width=135)
        self.treeview_services.heading('payment_status', text="Payment Status", command=lambda: self.treeview_sort_column(self.treeview_services, 'payment_status'))
        self.treeview_services.column('payment_status', anchor=tk.CENTER, width=140)

    def create_invoices_tv(self, root):
        """ Initialize invoices treeview. """
        self.invoice_columns = ('id', 'invoiced_date', 'due_date', 'amt_due', 'total_cost', 'carrier_name', 'status', 'paid_date', 'days_overdue')
        self.treeview_invoices = ttk.Treeview(root)
        self.treeview_invoices.configure(height=14, selectmode="extended", show="headings", columns=self.invoice_columns)
        self.treeview_invoices.bind("<Button-1>", self.treeview_click_handler)

        self.treeview_invoices.heading('id', text="ID", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'id'))
        self.treeview_invoices.column('id', anchor=tk.CENTER, width=50)
        self.treeview_invoices.heading('invoiced_date', text="Invoiced", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'invoiced_date'))
        self.treeview_invoices.column('invoiced_date', anchor=tk.CENTER, width=115)
        self.treeview_invoices.heading('due_date', text="Due", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'due_date'))
        self.treeview_invoices.column('due_date', anchor=tk.CENTER, width=115)
        self.treeview_invoices.heading('amt_due', text="Amount", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'amt_due'))
        self.treeview_invoices.column('amt_due', anchor=tk.CENTER, width=75)
        self.treeview_invoices.heading('total_cost', text="Total", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'total_cost'))
        self.treeview_invoices.column('total_cost', anchor=tk.CENTER, width=75)
        self.treeview_invoices.heading('carrier_name', text="Carrier", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'carrier_name'))
        self.treeview_invoices.column('carrier_name', anchor=tk.CENTER, width=140)
        self.treeview_invoices.heading('status', text="Status", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'status'))
        self.treeview_invoices.column('status', anchor=tk.CENTER, width=100)
        self.treeview_invoices.heading('paid_date', text="Date Paid", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'paid_date'))
        self.treeview_invoices.column('paid_date', anchor=tk.CENTER, width=115)
        self.treeview_invoices.heading('days_overdue', text="Days Overdue", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'days_overdue'))
        self.treeview_invoices.column('days_overdue', anchor=tk.CENTER, width=115)


if __name__ == "__main__":
    root = tk.Tk()
    widget = DataDisplayContainerUserWidget(root, test_data=True)
    # widget.pack(expand=True, fill="both")
    root.mainloop()
