#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import calendar
from datetime import datetime
from .utils import tk_center


class InvoiceMonthSelectionWidget(tk.Toplevel):
    def __init__(self, master=None, **kw):
        super(InvoiceMonthSelectionWidget,self).__init__(master,**kw)
        self.master = master
        
        self.section_title = tk.Frame(self)
        self.section_title.configure(height=25, width=960)
        self.lb_title = tk.Label(self.section_title)
        self.lb_title.configure(font="{Verdana} 10 {bold}", text='New Invoice')
        self.lb_title.place(x=15)
        self.section_title.pack(anchor="w", padx=10, pady=10, side="top")
        self.section_title.pack_propagate(0)
        self.line_selector = tk.LabelFrame(self)
        self.line_selector.configure(height=2, width=120)
        self.line_selector.place(x=15, y=35)
        self.form_frame = tk.Frame(self)
        self.form_frame.configure(height=200, width=200)
        self.lb_sel_info = tk.Label(self.form_frame)
        self.lb_sel_info.configure(
            font="{Verdana} 8 {}",
            text='Choose a month to be billed:')
        self.lb_sel_info.pack(anchor="w", padx=10, side="left")
        self.entry_month = ttk.Combobox(self.form_frame)
        self.entry_month.configure(
            justify="center",
            state="readonly",
            values="Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec")
        self.entry_month.current(datetime.now().month - 1)
        self.entry_month.pack(anchor="e", ipady=5, padx=10, side="left")
        self.form_frame.pack(anchor="w", padx=15, pady=10, side="top")
        self.control_container = tk.Frame(self)
        self.btn_generate = tk.Button(self.control_container)
        self.btn_generate.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            overrelief="ridge",
            relief="flat",
            takefocus=True,
            text='Generate ✓')
        self.btn_generate.pack(side="right")
        self.btn_generate.configure(command=self.form_submit)
        self.btn_cancel = tk.Button(self.control_container)
        self.btn_cancel.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            overrelief="ridge",
            relief="flat",
            text='× Cancel')
        self.btn_cancel.pack(padx=10, side="right")
        self.btn_cancel.configure(command=self.form_cancel)
        self.control_container.pack(
            anchor="e", padx=25, pady=15, side="bottom")
        self.configure(takefocus=True)
        self.geometry("320x160")
        self.resizable(False, False)
        self.title("New Invoice  - Healthcare Permanente")
        
        tk_center(self, gui_h=160, gui_w=320)
        
        self.ddc = self.master.calls(widget_name="ddc")

    def form_submit(self):
        selected = self.entry_month.get()
        self.destroy()
        abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
        self.ddc.toplevel_data_transfer_callback({'month': abbr_to_num[selected],
                                                  'mth_i': selected})

    def form_cancel(self):
        self.destroy()
        self.ddc.toplevel_callback()


if __name__ == "__main__":
    root = tk.Tk()
    widget = InvoiceMonthSelectionWidget(root)
    # widget.pack(expand=True, fill="both")
    root.mainloop()
