#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox, StringVar
from tkcalendar import Calendar # external package -> 'pip install tkcalendar' to install
from .utils import tk_center


class ServiceAddToplvlWidget(tk.Toplevel):
    def __init__(self, master=None, **kw):
        super(ServiceAddToplvlWidget,self).__init__(master,**kw)
        self.master = master
        
        self.section_title = tk.Frame(self)
        self.section_title.configure(height=25, width=960)
        self.lb_title = tk.Label(self.section_title)
        self.lb_title.configure(
            font="{Verdana} 10 {bold}",
            text='Adding new Service')
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
        self.lb_description = tk.Label(self.lb_frame)
        self.lb_description.configure(
            font="{Verdana} 8 {}",
            text='Service description:',
            width=20)
        self.lb_description.pack(padx=10, side="top")
        self.lb_date = tk.Label(self.lb_frame)
        self.lb_date.configure(
            font="{Verdana} 8 {}",
            text='Service date:',
            width=20)
        self.lb_date.pack(padx=10, pady=30, side="top")
        self.lb_cost = tk.Label(self.lb_frame)
        self.lb_cost.configure(
            font="{Verdana} 8 {}",
            text='Service cost:',
            width=20)
        self.lb_cost.pack(padx=10, side="top")
        self.lb_frame.pack(side="left")
        self.entry_frame = tk.Frame(self.form_frame)
        self.entry_frame.configure(height=200, width=200)
        self.entry_description = tk.Entry(self.entry_frame)
        self.entry_description.configure(
            font="{Verdana} 9 {}", justify="left", width=50)
        self.entry_description.pack(ipady=5, side="top")
        
        self.cal = Calendar(self, date_pattern="mm/dd/yyyy")
        self.bind("<<CalendarSelected>>", self.calendar_selection)
        
        self.entry_date = tk.Entry(self.entry_frame)
        self.entry_date.configure(
            font="{Verdana} 9 {}",
            justify="left",
            width=20)
        self.entry_date.insert(0, self.cal.get_date())
        self.entry_date.bind("<FocusIn>", self.show_calendar)
        self.entry_date.bind("<FocusOut>", self.hide_calendar)
        self.entry_date.pack(ipady=5, pady=20, side="top")
        
        self.cost_frame = tk.Frame(self.entry_frame)
        self.cost_frame.configure(height=200, width=200)
        self.lb_dollar_sign = tk.Label(self.cost_frame)
        self.lb_dollar_sign.configure(font="{Verdana} 10 {}", text='$')
        self.lb_dollar_sign.pack(anchor="e", padx=5, side="left")
        
        self.entry_cost_value = StringVar()
        self.entry_cost_value.trace_add("write", self.cost_entry_upd)
        self.entry_cost = tk.Entry(self.cost_frame, textvariable=self.entry_cost_value)
        self.entry_cost.configure(
            font="{Verdana} 9 {}",
            justify="left",
            width=10)
        self.entry_cost.pack(ipady=5, side="bottom")
        self.cost_frame.pack(side="top")
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
            relief="flat",
            takefocus=True,
            text='Done ✓')
        self.btn_done.pack(side="right")
        self.btn_done.configure(command=self.form_submit)
        self.btn_cancel = tk.Button(self.control_container)
        self.btn_cancel.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            relief="flat",
            text='× Cancel')
        self.btn_cancel.pack(padx=10, side="right")
        self.btn_cancel.configure(command=self.form_cancel)
        self.control_container.pack(
            anchor="e", padx=30, pady=20, side="bottom")
        self.geometry("640x260")
        self.resizable(False, False)
        self.title("Adding new service - Healthcare Permanente")
        self.protocol("WM_DELETE_WINDOW", self.form_cancel)
        
        self.lb_warning = tk.Label(self)
        self.lb_warning.configure(font="{Verdana} 8 {bold}", fg='#ffaa00', 
                                  text="Only digits (0-9) and ',.' are allowed here.")
        
        tk_center(self, gui_w=640, gui_h=260)
        
    def cost_entry_upd(self, *event):
        value = self.entry_cost_value.get()
        if value == ".": return
        if not value.replace(" ", 'S').replace(".,",'E').replace(",", "").replace(".","",1).isnumeric():
            x, y = self.cost_frame.winfo_x(), self.cost_frame.winfo_y()
            self.lb_warning.configure(text="Only digits (0-9) and ',.' are allowed here.")
            self.lb_warning.place(x=x*1.9, y=y+85)
        else:
            if "." in value:
                if len(value[value.find(".")+1:]) > 2:
                    x, y = self.cost_frame.winfo_x(), self.cost_frame.winfo_y()
                    self.lb_warning.configure(text="Cent part should only have at most 2 digits.")
                    self.lb_warning.place(x=x*1.9, y=y+85)
                    return
            self.lb_warning.place_forget()
            
    def calendar_selection(self, event=None):
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, self.cal.get_date())

    def show_calendar(self, event=None):
        x = max(426, self.winfo_pointerx() - self.winfo_rootx())
        y = self.winfo_pointery() - self.winfo_rooty()
        self.cal.place(x=x,y=y)
        if x > 380:
            self.geometry(f"{640 + x-380}x360")
        else:
            self.geometry("640x360")
            
    def hide_calendar(self, event=None):
        self.geometry("640x260")
        self.cal.place_forget()    

    def form_submit(self):
        data = {'description': self.entry_description.get(), 
                'date': self.entry_date.get(), 
                'cost': "$" + self.entry_cost.get()}
        if not any(data.values()):
            messagebox.showwarning("Warning", "Make sure to fill out all fields before continue.")    
        else:
            self.destroy()
            self.master.toplevel_data_transfer_callback(data)
        
    def form_cancel(self):
        if messagebox.askyesno("Quit", "You have unsaved changes. Are you sure you want to close this window?"):
            self.destroy()
            self.master.toplevel_callback()
    
if __name__ == "__main__":
    root = tk.Tk()
    widget = ServiceAddToplvlWidget(root)
    # widget.pack(expand=True, fill="both")
    widget.mainloop()
