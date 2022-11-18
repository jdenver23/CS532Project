#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from data_display_container_carrier_add_toplvl import CarrierAddToplvlWidget
from data_display_container_service_add_toplvl import ServiceAddToplvlWidget


class DataDisplayContainerWidget(tk.Frame):
    def __init__(self, master=None, test_data=False, **kw):
        super(DataDisplayContainerWidget, self).__init__(master, **kw)
        self.master = master
        
        self.section_title = tk.Frame(self)
        self.section_title.configure(height=25, width=960)
        self.title_carriers = tk.Label(self.section_title)
        self.title_carriers.configure(
            font="{Verdana} 10 {bold}", text='Carriers')
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
        self.active_treeview = "Carriers"
        
        if test_data: self.add_test_data()
        
        treeview_style = ttk.Style()
        treeview_style.configure("Treeview.Heading", font="{Verdana} 10 {}")
        treeview_style.configure('Treeview', rowheight=25)
        
        self.treeview_fr.pack(anchor="n", padx=10, pady=10, side="top")
        
        self.control_container = tk.Frame(self)
        self.btn_delete = tk.Button(self.control_container)
        self.btn_delete.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            relief="flat",
            state="disabled",
            takefocus=True,
            text='× Delete')
        self.btn_delete.pack(side="right")
        self.btn_delete.configure(command=lambda: self.treeview_del_selection())
        self.btn_add = tk.Button(self.control_container)
        self.btn_add.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            relief="flat",
            takefocus=True,
            text='+ Add')
        self.btn_add.pack(padx=10, side="right")
        self.btn_add.configure(command=lambda: self.treeview_add_item_window())
        
        self.control_container.pack(anchor="n", padx=30, side="right")
        
        self.configure(height=550, width=960)
        self.pack_propagate(0)
        self.master.bind("<Tab>", self.toggle_treeview_tab)
    
    def toggle_treeview_tab(self, event=None):
        idx = 0
        if self.active_treeview == "Services":
            idx = 1
        elif self.active_treeview == "Invoices":
            idx = 2
        self.toggle_treeview(index=idx)
    
    def toplevel_callback(self, toplevel, data=None):
        # TODO: add data to local list
        self.master.deiconify()
        self.treeview_add_item(data)
        self.master.add_data(data)
        
    def treeview_add_item(self, data):
        if self.active_treeview == "Carriers":
            # TODO: send data back to main
            self.treeview_insert_row(self.treeview_carriers, [['9'] + data])
        elif self.active_treeview == "Services":
            self.treeview_insert_row(self.treeview_services, [['8'] + data])
        elif self.active_treeview == "Invoices":
            pass
        
    def treeview_add_item_window(self):
        if self.active_treeview == "Carriers":
            CarrierAddToplvlWidget(self)
            self.master.withdraw()
        elif self.active_treeview == "Services":
            ServiceAddToplvlWidget(self)
            self.master.withdraw()            
        elif self.active_treeview == "Invoices":
            pass
    
    def treeview_del_selection(self):
        # TODO: remove data from local list
        if self.active_treeview == "Carriers":
            selection = self.treeview_carriers.selection()
            selection_i = self.treeview_carriers.item(selection)
            self.treeview_carriers.delete(*selection)
            
        elif self.active_treeview == "Services":
            selection = self.treeview_services.selection()
            selection_i = self.treeview_services.item(selection)
            self.treeview_services.delete(*selection)
            
        elif self.active_treeview == "Invoices":
            selection = self.treeview_invoices.selection()
            selection_i = self.treeview_invoices.item(selection)
            self.treeview_invoices.delete(*selection)
            
        self.btn_delete.configure(state=tk.DISABLED)
    
    def create_carriers_tv(self, root):
        self.carrier_columns = ('id','name','address','primary')
        self.treeview_carriers = ttk.Treeview(root)
        self.treeview_carriers.configure(
            height=14, selectmode="extended", show="headings", columns=self.carrier_columns)
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
        self.service_columns = ('id','description', 'date','cost')
        self.treeview_services = ttk.Treeview(root)
        self.treeview_services.configure(
            height=14, selectmode="extended", show="headings", columns=self.service_columns)
        self.treeview_services.bind("<Button-1>", self.treeview_click_handler)
        
        self.treeview_services.heading('id', text="ID", command=lambda: self.treeview_sort_column(self.treeview_services, 'id'))
        self.treeview_services.column('id', anchor=tk.CENTER, width=50)
        self.treeview_services.heading('description', text="Description", command=lambda: self.treeview_sort_column(self.treeview_services, 'description'))
        self.treeview_services.column('description', anchor=tk.CENTER, width=580)
        self.treeview_services.heading('date', text="Date", command=lambda: self.treeview_sort_column(self.treeview_services, 'date'))
        self.treeview_services.column('date', anchor=tk.CENTER, width=135)
        self.treeview_services.heading('cost', text="Cost", command=lambda: self.treeview_sort_column(self.treeview_services, 'cost'))
        self.treeview_services.column('cost', anchor=tk.CENTER, width=135)
        
    def create_invoices_tv(self, root):
        # TODO: invoiced services will be in a different container
        self.invoice_columns = ('id','invoiced_date','due_date','amt_due','carrier_name','status','paid_date','days_overdue')
        self.treeview_invoices = ttk.Treeview(root)
        self.treeview_invoices.configure(
            height=14, selectmode="extended", show="headings", columns=self.invoice_columns)
        self.treeview_invoices.bind("<Button-1>", self.treeview_click_handler)
        
        self.treeview_invoices.heading('id', text="ID", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'id'))
        self.treeview_invoices.column('id', anchor=tk.CENTER, width=50)
        self.treeview_invoices.heading('invoiced_date', text="Invoiced", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'invoiced_date'))
        self.treeview_invoices.column('invoiced_date', anchor=tk.CENTER, width=135)
        self.treeview_invoices.heading('due_date', text="Due", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'due_date'))
        self.treeview_invoices.column('due_date', anchor=tk.CENTER, width=135)
        self.treeview_invoices.heading('amt_due', text="Amount", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'amt_due'))
        self.treeview_invoices.column('amt_due', anchor=tk.CENTER, width=75)
        self.treeview_invoices.heading('carrier_name', text="Carrier", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'carrier_name'))
        self.treeview_invoices.column('carrier_name', anchor=tk.CENTER, width=135)
        self.treeview_invoices.heading('status', text="Status", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'status'))
        self.treeview_invoices.column('status', anchor=tk.CENTER, width=100)
        self.treeview_invoices.heading('paid_date', text="Date Paid", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'paid_date'))
        self.treeview_invoices.column('paid_date', anchor=tk.CENTER, width=135)
        self.treeview_invoices.heading('days_overdue', text="Days Overdue", command=lambda: self.treeview_sort_column(self.treeview_invoices, 'days_overdue'))
        self.treeview_invoices.column('days_overdue', anchor=tk.CENTER, width=135)
        
    def treeview_sort_column(self, treeview, col, reverse=True):
        l = [(treeview.set(k, col), k) for k in treeview.get_children('')]
        l.sort(key=lambda x: x[0], reverse=reverse)

        for index, (val, k) in enumerate(l):
            treeview.move(k, '', index)

        treeview.heading(col, command=lambda: self.treeview_sort_column(treeview, col, not reverse))
        
    def treeview_forced_set_state(self, treeview: ttk.Treeview, show=False):
        if not show: 
            treeview.pack_forget()
        else:
            treeview.pack(expand="true", fill="x", padx=10, pady=10, side="top")
        
    def toggle_treeview(self, event: tk.Event = None, index = None):
        if index == 0 or event.widget.cget("text") == "Carriers":
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
        elif index == 1 or event.widget.cget("text") == "Services":
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
            self.line_selector.place(x=120, y=35)
            self.title_invoices.place(x=180, y=0)
        elif index == 2 or event.widget.cget("text") == "Invoices":
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
            self.line_selector.place(x=203, y=35)
        
        self.selected_item_id = ""
        self.selected_row = ""
        self.btn_delete.configure(state=tk.DISABLED)
    
    def treeview_insert_row(self, treeview: ttk.Treeview, list_rows: list(list())):
        for row in list_rows:
            treeview.insert("", tk.END, values=row)
    
    def treeview_click_handler(self, event):
        if event.widget.identify_region(event.x, event.y) == "separator":
            return "break"
        self.selected_item_id = event.widget.identify('item', event.x, event.y)
        self.selected_row = event.widget.item(self.selected_item_id)['values']
        if self.selected_item_id != "" and event.widget.exists(self.selected_item_id):
            self.btn_delete.configure(state=tk.NORMAL)
        else:
            self.treeview_carriers.selection_remove(*self.treeview_carriers.selection())
            self.treeview_services.selection_remove(*self.treeview_services.selection())
            self.treeview_invoices.selection_remove(*self.treeview_invoices.selection())
            self.btn_delete.configure(state=tk.DISABLED)
            
    def add_test_data(self):
        self.treeview_insert_row(self.treeview_carriers, [['2', 'a', '789', 'NON-PRIMARY'],
                                                          ['0', 'c', '123', 'PRIMARY'],
                                                          ['3', 'b', 'Street', 'NON-PRIMARY'],
                                                          ['1', 'd', '456', 'NON-PRIMARY'],])
        self.treeview_insert_row(self.treeview_services, [['4', 'e', 'FDSF', '$12'],
                                                          ['5', 'f', 'jd5r', '$888'],
                                                          ['6', 'g', 'io', '$1'],
                                                          ['7', 'h', '#$456', '$65'],])
        self.treeview_insert_row(self.treeview_invoices, [['0', '1-1-2001', '2-1-2001', '$1200', 'test carrier', 'UNPAID', '', '123'],])
    

if __name__ == "__main__":
    root = tk.Tk()
    widget = DataDisplayContainerWidget(root, test_data=True)
    widget.pack(expand=True, fill="both")
    root.mainloop()
