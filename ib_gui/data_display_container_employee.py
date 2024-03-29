#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from .data_display_container_carrier_addedit_toplvl import CarrierAddEditToplvlWidget
from .data_display_container_service_addedit_toplvl import ServiceAddEditToplvlWidget
from .data_display_container_invoice_month_selection import InvoiceMonthSelectionWidget
from .data_display_container_invoice_view import InvoiceViewWidget
from .data_display_container_reports_view import ReportsViewWidget
from InsuranceBilling import InsuranceBilling, InsuranceInvoice, dollar_to_float


class DataDisplayContainerEmployeeWidget(tk.Frame):
    def __init__(self, bill: InsuranceBilling, master=None, test_data=False, **kw):
        super(DataDisplayContainerEmployeeWidget, self).__init__(master, **kw)
        self.bill: InsuranceBilling = bill

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
        
        self.btn_viewedit = tk.Button(self.control_container)
        self.btn_viewedit.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            state="disabled",
            overrelief="ridge",
            text='ⓘ Edit')
        self.btn_viewedit.pack(ipadx=5, ipady=5, side="left")
        self.btn_viewedit.configure(command=lambda: self.treeview_edit_selection())
        self.btn_delete = tk.Button(self.control_container)
        self.btn_delete.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            state="disabled",
            overrelief="ridge",
            text='× Delete')
        self.btn_delete.pack(ipadx=5, ipady=5, padx=10, side="left")
        self.btn_delete.configure(command=lambda: self.treeview_del_selection())
        
        self.btn_add = tk.Button(self.control_container)
        self.btn_add.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            takefocus=True,
            overrelief="ridge",
            text='+ Add')
        self.btn_add.pack(ipadx=5, ipady=5, padx=10, side="right")
        self.btn_add.configure(command=lambda: self.treeview_add_item_window())
        
        self.btn_mark_as = tk.Button(self.control_container)
        self.btn_mark_as.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            state="disabled",
            overrelief="ridge")
        self.btn_mark_as.configure(command=lambda: self.selection_mark_as())
        
        self.btn_generate_reports = tk.Button(self.control_container)
        self.btn_generate_reports.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            overrelief="ridge",
            text="Generate Reports")
        self.btn_generate_reports.configure(command=lambda: self.generate_reports())

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
    
    def generate_reports(self):
        self.master.attributes("-disabled", True)
        self.toplevel_force_focus_fid = self.master.bind("<Button-1>", self.toplevel_force_focus)
        self.curr_toplvl = ReportsViewWidget(master=self.master, bill=self.bill)
    
    def selection_mark_as(self):
        if self.active_treeview == "Carriers":
            for selection in self.treeview_carriers.selection():
                item_vals = self.treeview_carriers.item(selection)['values']
                _id_to_edit = item_vals[0]
                _to_edit = self.bill.get_carrier(_id_to_edit)
                if item_vals[3] == "NON-PRIMARY":
                    # set to primary
                    self.bill.set_primary(_id_to_edit, True)
                    self.btn_mark_as.configure(text="✓ Mark as NON-PRIMARY")
                    
                    for child in self.treeview_carriers.get_children():
                        self.treeview_carriers.set(child, column="primary", value="NON-PRIMARY")
                        
                    self.treeview_carriers.set(selection, column="primary", value="PRIMARY")
                else:
                    # set to non-primary
                    self.bill.set_primary(_id_to_edit, False)
                    self.btn_mark_as.configure(text="✓ Mark as PRIMARY")
                    
                    last_child = self.treeview_carriers.get_children()[-1]
                    if last_child == selection and len(self.treeview_carriers.get_children()) > 1:
                        last_child = self.treeview_carriers.get_children()[-2]
                    
                    if len(self.treeview_carriers.get_children()) == 1:
                        self.btn_mark_as.configure(text="✓ Mark as NON-PRIMARY")
                        self.treeview_carriers.set(selection, column="primary", value="PRIMARY")
                    else:
                        self.treeview_carriers.set(last_child, column="primary", value="PRIMARY")
                        self.treeview_carriers.set(selection, column="primary", value="NON-PRIMARY")
                
        elif self.active_treeview == "Services":
            for selection in self.treeview_services.selection():
                item_vals = self.treeview_services.item(selection)['values']
                _to_edit = self.bill.get_service(item_vals[0])
                if item_vals[4] == "UNPAID":
                    _to_edit.mark_as_paid()
                    self.btn_mark_as.configure(text="✓ Mark as UNPAID")
                else:
                    _to_edit.mark_as_unpaid()
                    self.btn_mark_as.configure(text="✓ Mark as PAID")
                self.treeview_services.item(selection, values=_to_edit.as_list())
                
        elif self.active_treeview == "Invoices":
            for selection in self.treeview_invoices.selection():
                item_vals = self.treeview_invoices.item(selection)['values']
                _to_edit = self.bill.get_invoice(item_vals[0])
                if item_vals[6] == "UNPAID":
                    self.bill.pay_for_invoice(item_vals[0], pay_in_full=True)
                    self.btn_mark_as.configure(text="✓ Mark as UNPAID")
                else:
                    self.bill.reset_invoice(item_vals[0])
                    self.btn_mark_as.configure(text="✓ Mark as PAID")
                self.treeview_invoices.item(selection, values=_to_edit.as_list())
            

    def pull_from_db(self, refresh=True, renew_carriers=True, renew_services=True, renew_invoices=True):
        self.btn_delete.configure(state=tk.DISABLED)
        self.btn_viewedit.configure(state=tk.DISABLED)
        self.btn_mark_as.configure(state=tk.DISABLED)
        
        # remove all children from all treeviews
        if renew_carriers: self.treeview_carriers.delete(*self.treeview_carriers.get_children())
        if renew_services: self.treeview_services.delete(*self.treeview_services.get_children())
        if renew_invoices: self.treeview_invoices.delete(*self.treeview_invoices.get_children())

        if self.bill is not None:
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
    
    def toplevel_data_edit_callback(self, data: dict):
        """`DDC` data edit call back."""
        self.reset_attributes()
        
        if any(data.values()) and hasattr(self, "id_to_edit"):
            if self.active_treeview == "Carriers":
                self.bill.edit_carrier(carrier_id=self.id_to_edit, n_primary=data['primary']=="PRIMARY", n_address=data['address'], n_name=data['name'])
                self.treeview_carriers.item(self.curr_selected, values=[self.id_to_edit] + list(data.values()))
                
                for child in self.treeview_carriers.get_children():
                    if child == self.curr_selected: 
                        continue
                    _curr_id = self.treeview_carriers.item(child)['values'][0]
                    self.treeview_carriers.item(child, values=self.bill.get_carrier(_curr_id).as_list())
                    
            elif self.active_treeview == "Services":
                self.bill.edit_service(service_id=self.id_to_edit, n_description=data['description'], n_cost=data['cost'], n_date=data['date'])
                self.treeview_services.item(self.curr_selected, values=[self.id_to_edit] + list(data.values()))
        
    def toplevel_data_transfer_callback(self, data: dict):
        """`DDC` data transfer (add) call back."""
        self.reset_attributes()
        
        if any(data.values()):
            if self.active_treeview == "Carriers":
                n_data = self.bill.new_carrier(data['name'], data['address'], data['primary'] == "PRIMARY")
                if data['primary'] == "PRIMARY":
                    self.pull_from_db(refresh=False)
                else:
                    self.treeview_insert_row(self.treeview_carriers, [n_data.as_list()])
            elif self.active_treeview == "Services":
                n_data = self.bill.new_service(data['description'], data['cost'], data['date'])
                self.treeview_insert_row(self.treeview_services, [n_data.as_list()])
            elif self.active_treeview == "Invoices":
                n_return = self.bill.generate_invoice(data['month'])
                if n_return == -1:
                    messagebox.showwarning("Warning", f"Could not generate invoice (no services found in {data['mth_i']} or all services were paid!)")
                elif n_return == -2:
                    messagebox.showwarning("Warning", f"Could not generate invoice (no primary/non-primary carriers found for {self.bill.user_name})")
                
                if type(n_return) == InsuranceInvoice:
                    self.pull_from_db(refresh=False, renew_carriers=False, renew_services=False)
    
    def toplevel_force_focus(self, event=None):
        if hasattr(self, "curr_toplvl"):
            self.curr_toplvl.focus_force()
            return "break"
    
    def treeview_reset_sel(self):
        self.treeview_carriers_curr_sel = None
        self.treeview_services_curr_sel = None
        self.treeview_invoices_curr_sel = None
        
    def toggle_treeview_item(self, direction="down", event=None):
        """ Handle keybind events to navigate through treeviews and its items. """
        dx = -1 if direction == "up" else 1
        
        if self.active_treeview == "Carriers":
            if self.treeview_carriers_curr_sel is None: self.treeview_carriers_curr_sel = 0 if dx == 1 else -1
            else: self.treeview_carriers_curr_sel += dx
            all_child = self.treeview_carriers.get_children()
            if len(all_child) == 0: return
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
            if len(all_child) == 0: return
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
            if len(all_child) == 0: return
            if self.treeview_invoices_curr_sel >= len(all_child):
                self.treeview_invoices_curr_sel = 0
            elif self.treeview_invoices_curr_sel < 0: 
                self.treeview_invoices_curr_sel = len(all_child)-1
            self.selected_item_id = all_child[self.treeview_invoices_curr_sel]
            self.treeview_invoices.selection_set(self.selected_item_id)
            self.treeview_sel_handler()

    def treeview_add_item_window(self):
        self.master.attributes("-disabled", True)
        self.toplevel_force_focus_fid = self.master.bind("<Button-1>", self.toplevel_force_focus)
        
        if self.active_treeview == "Carriers":
            self.curr_toplvl = CarrierAddEditToplvlWidget(self.master)
        elif self.active_treeview == "Services":
            self.curr_toplvl = ServiceAddEditToplvlWidget(self.master)
        elif self.active_treeview == "Invoices":
            self.curr_toplvl = InvoiceMonthSelectionWidget(self.master)
    
    def treeview_edit_selection(self) -> None:
        self.master.attributes("-disabled", True)
        self.toplevel_force_focus_fid = self.master.bind("<Button-1>", self.toplevel_force_focus)
        
        if self.active_treeview == "Carriers":
            self.curr_selected = self.treeview_carriers.selection()[0]
            self.id_to_edit = self.treeview_carriers.item(self.curr_selected)['values'][0]
            self.curr_toplvl = CarrierAddEditToplvlWidget(master=self.master, carrier=self.bill.get_carrier(self.id_to_edit))

        elif self.active_treeview == "Services":
            self.curr_selected = self.treeview_services.selection()[0]
            self.id_to_edit = self.treeview_services.item(self.curr_selected)['values'][0]
            self.curr_toplvl = ServiceAddEditToplvlWidget(master=self.master, service=self.bill.get_service(self.id_to_edit))

        elif self.active_treeview == "Invoices":
            self.curr_selected = self.treeview_invoices.selection()[0]
            self.id_to_edit = self.treeview_invoices.item(self.curr_selected)['values'][0]
            self.curr_toplvl = InvoiceViewWidget(master=self.master, invoice=self.bill.get_invoice(self.id_to_edit), bill=self.bill)

    def treeview_del_selection(self):
        if self.active_treeview == "Carriers":
            selections = self.treeview_carriers.selection()
            for selection in selections:
                id_to_remove = self.treeview_carriers.item(selection)['values'][0]
                self.bill.remove_carrier(id_to_remove)

            self.treeview_carriers.delete(*selections)

        elif self.active_treeview == "Services":
            selections = self.treeview_services.selection()
            for selection in selections:
                id_to_remove = self.treeview_services.item(selection)['values'][0]
                self.bill.remove_service(id_to_remove)

            self.treeview_services.delete(*selections)

        elif self.active_treeview == "Invoices":
            selections = self.treeview_invoices.selection()
            for selection in selections:
                id_to_remove = self.treeview_invoices.item(selection)['values'][0]
                self.bill.remove_invoice(id_to_remove)

            self.treeview_invoices.delete(*selections)

        self.btn_delete.configure(state=tk.DISABLED)
        self.btn_viewedit.configure(state=tk.DISABLED)
        self.btn_mark_as.configure(state=tk.DISABLED)

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
    
    def treeview_sel_handler(self):
        if self.selected_item_id != "":
            self.btn_delete.configure(state=tk.NORMAL)
            self.btn_viewedit.configure(state=tk.NORMAL)
            self.btn_mark_as.configure(state=tk.NORMAL)
            self.btn_generate_reports.configure(state=tk.NORMAL)
            
            if self.active_treeview == "Carriers":
                is_carrier_primary = self.treeview_carriers.item(self.selected_item_id)['values'][3] == "PRIMARY"
                if is_carrier_primary:
                    self.btn_mark_as.configure(text="✓ Mark as NON-PRIMARY")
                elif not is_carrier_primary:
                    self.btn_mark_as.configure(text="✓ Mark as PRIMARY")
                    
            elif self.active_treeview == "Services":
                is_service_paid = self.treeview_services.item(self.selected_item_id)['values'][4] == "PAID"
                if is_service_paid:
                    self.btn_mark_as.configure(text="✓ Mark as UNPAID")
                elif not is_service_paid:
                    self.btn_mark_as.configure(text="✓ Mark as PAID")
                    
            elif self.active_treeview == "Invoices":
                is_invoice_paid = self.treeview_invoices.item(self.selected_item_id)['values'][6] == "PAID"
                if is_invoice_paid:
                    self.btn_mark_as.configure(text="✓ Mark as UNPAID")
                elif not is_invoice_paid:
                    self.btn_mark_as.configure(text="✓ Mark as PAID")
            
            self.btn_mark_as.pack(padx=10, ipadx=5, ipady=5, side="right")
            
        else:
            self.btn_delete.configure(state=tk.DISABLED)
            self.btn_viewedit.configure(state=tk.DISABLED)
            self.btn_mark_as.configure(state=tk.DISABLED)

    def treeview_click_handler(self, event):
        # disable column resizing by disable mouse click at "separator"
        if event.widget.identify_region(event.x, event.y) == "separator":
            return "break"
        
        # `btn_delete` custom behaviour
        self.selected_item_id = event.widget.identify('item', event.x, event.y)
        self.selected_row = event.widget.item(self.selected_item_id)['values']
        if self.selected_item_id != "" and event.widget.exists(self.selected_item_id):
            self.treeview_sel_handler()            
        else:
            self.treeview_carriers.selection_remove(*self.treeview_carriers.selection())
            self.treeview_services.selection_remove(*self.treeview_services.selection())
            self.treeview_invoices.selection_remove(*self.treeview_invoices.selection())
            self.btn_delete.configure(state=tk.DISABLED)
            self.btn_viewedit.configure(state=tk.DISABLED)
            self.btn_mark_as.configure(state=tk.DISABLED)

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
            self.btn_viewedit.configure(text="ⓘ Edit")
            self.btn_mark_as.pack_forget()
            self.btn_generate_reports.pack_forget()
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
            self.btn_viewedit.configure(text="ⓘ Edit")
            self.btn_mark_as.pack_forget()
            self.btn_generate_reports.pack_forget()
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
            self.btn_viewedit.configure(text="ⓘ View")
            self.btn_mark_as.pack_forget()
            self.btn_generate_reports.pack(ipadx=5, ipady=5, side="left")

        self.selected_item_id = ""
        self.selected_row = ""
        self.btn_delete.configure(state=tk.DISABLED)
        self.btn_viewedit.configure(state=tk.DISABLED)
        self.btn_mark_as.configure(state=tk.DISABLED)

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
        """ Initialize services treeview. """
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
    widget = DataDisplayContainerEmployeeWidget(root, test_data=True)
    # widget.pack(expand=True, fill="both")
    root.mainloop()
