#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class DataDisplayContainerWidget(tk.Frame):
    def __init__(self, master=None, **kw):
        super(DataDisplayContainerWidget, self).__init__(master, **kw)
        
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
        
        self.left_pad = tk.Label(self)
        self.left_pad.configure(justify="left")
        self.left_pad.pack(anchor="w", side="left")
        self.right_pad = tk.Label(self)
        self.right_pad.configure(justify="left")
        self.right_pad.pack(anchor="e", side="right")
        
        self.create_carriers_tv()
        self.create_services_tv()
        self.create_invoices_tv()
        self.treeview_forced_set_state(self.treeview_carriers, show=True)
        self.active_treeview = "Carriers"
        
        treeview_style = ttk.Style()
        treeview_style.configure("Treeview.Heading", font="{Verdana} 10 {}")
        treeview_style.configure('Treeview', rowheight=25)
        
        self.control_container = tk.Frame(self)
        self.btn_delete = tk.Button(self.control_container)
        self.btn_delete.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 12 {}",
            foreground="white",
            justify="left",
            relief="flat",
            state="disabled",
            takefocus=True,
            text='× Delete')
        self.btn_delete.pack(side="right")
        self.btn_add = tk.Button(self.control_container)
        self.btn_add.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 12 {}",
            foreground="white",
            justify="left",
            relief="flat",
            takefocus=True,
            text='+ Add')
        self.btn_add.pack(padx=10, side="right")
        self.control_container.pack(ipadx=960, padx=10, pady=10, side="bottom")
        self.configure(height=500, width=960)
        self.pack_propagate(0)
        
    
    def create_carriers_tv(self):
        self.carrier_columns = ('name','address','primary')
        self.treeview_carriers = ttk.Treeview(self)
        self.treeview_carriers.configure(
            height=14, selectmode="extended", show="headings", columns=self.carrier_columns)
        self.treeview_carriers.bind("<Button-1>", self.treeview_click_handler)
        
        self.treeview_carriers.pack(pady=10, side="top")
        self.treeview_carriers.heading('name', text="Name")
        self.treeview_carriers.column('name', anchor=tk.CENTER, width=400)
        self.treeview_carriers.heading('address', text="Address")
        self.treeview_carriers.column('address', anchor=tk.CENTER, width=300)
        self.treeview_carriers.heading('primary', text="Primary")
        self.treeview_carriers.column('primary', anchor=tk.CENTER, width=145)
        
        self.treeview_carriers.pack_forget()
        
    def create_services_tv(self):
        self.service_columns = ('description', 'date','cost')
        self.treeview_services = ttk.Treeview(self)
        self.treeview_services.configure(
            height=14, selectmode="extended", show="headings", columns=self.service_columns)
        self.treeview_services.bind("<Button-1>", self.treeview_click_handler)
        
        self.treeview_services.pack(pady=10, side="top")
        self.treeview_services.heading('description', text="Description")
        self.treeview_services.column('description', anchor=tk.CENTER, width=400)
        self.treeview_services.heading('date', text="Date")
        self.treeview_services.column('date', anchor=tk.CENTER, width=200)
        self.treeview_services.heading('cost', text="Cost")
        self.treeview_services.column('cost', anchor=tk.CENTER, width=145)
        
        self.treeview_services.pack_forget()
        
    def create_invoices_tv(self):
        # TODO: invoiced services will be in a different container
        self.invoice_columns = ('id','invoiced_date','due_date','carrier_name','amt_due','status','paid_date','days_overdue')
        self.treeview_invoices = ttk.Treeview(self)
        self.treeview_invoices.configure(
            height=14, selectmode="extended", show="headings", columns=self.invoice_columns)
        self.treeview_invoices.bind("<Button-1>", self.treeview_click_handler)
        
        self.treeview_invoices.pack(pady=10, side="top")
        self.treeview_invoices.heading('id', text="ID")
        self.treeview_invoices.column('id', anchor=tk.CENTER, width=50)
        self.treeview_invoices.heading('invoiced_date', text="Invoiced")
        self.treeview_invoices.column('invoiced_date', anchor=tk.CENTER, width=145)
        self.treeview_invoices.heading('due_date', text="Due")
        self.treeview_invoices.column('due_date', anchor=tk.CENTER, width=145)
        self.treeview_invoices.heading('carrier_name', text="Carrier")
        self.treeview_invoices.column('carrier_name', anchor=tk.CENTER, width=145)
        self.treeview_invoices.heading('amt_due', text="Amount")
        self.treeview_invoices.column('amt_due', anchor=tk.CENTER, width=75)
        self.treeview_invoices.heading('status', text="Status")
        self.treeview_invoices.column('status', anchor=tk.CENTER, width=75)
        self.treeview_invoices.heading('paid_date', text="Date Paid")
        self.treeview_invoices.column('paid_date', anchor=tk.CENTER, width=145)
        self.treeview_invoices.heading('days_overdue', text="Days Overdue")
        self.treeview_invoices.column('days_overdue', anchor=tk.CENTER, width=145)
        
        self.treeview_invoices.pack_forget()
        
    def treeview_forced_set_state(self, treeview: ttk.Treeview, show=False):
        if not show: 
            treeview.pack_forget()
        else:
            treeview.pack(expand="true", fill="x", padx=10, pady=10, side="top")
        
    def toggle_treeview(self, event: tk.Event):
        if event.widget.cget("text") == "Carriers":
            self.title_carriers.config(font="{Verdana} 10 {bold}")
            self.title_services.config(font="{Verdana} 10 {}")
            self.title_invoices.config(font="{Verdana} 10 {}")
            self.treeview_forced_set_state(self.treeview_carriers, show=True)
            self.treeview_forced_set_state(self.treeview_services, show=False)
            self.treeview_forced_set_state(self.treeview_invoices, show=False)
            self.line_selector.place(x=40, y=35)
        elif event.widget.cget("text") == "Services":
            self.active_treeview = "Services"
            self.title_carriers.config(font="{Verdana} 10 {}")
            self.title_services.config(font="{Verdana} 10 {bold}")
            self.title_invoices.config(font="{Verdana} 10 {}")
            self.treeview_forced_set_state(self.treeview_carriers, show=False)
            self.treeview_forced_set_state(self.treeview_services, show=True)
            self.treeview_forced_set_state(self.treeview_invoices, show=False)
            self.line_selector.place(x=120, y=35)
        elif event.widget.cget("text") == "Invoices":
            self.active_treeview = "Invoices"
            self.title_carriers.config(font="{Verdana} 10 {}")
            self.title_services.config(font="{Verdana} 10 {}")
            self.title_invoices.config(font="{Verdana} 10 {bold}")
            self.treeview_forced_set_state(self.treeview_carriers, show=False)
            self.treeview_forced_set_state(self.treeview_services, show=False)
            self.treeview_forced_set_state(self.treeview_invoices, show=True)
            self.line_selector.place(x=198, y=35)
    
    def treeview_insert_row(self, treeview: ttk.Treeview, list_rows: list(list())):
        for row in list_rows:
            treeview.insert("", tk.END, values=row)
    
    def treeview_click_handler(self, event):
        if event.widget.identify_region(event.x, event.y) == "separator":
            return "break"

if __name__ == "__main__":
    root = tk.Tk()
    widget = DataDisplayContainerWidget(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

