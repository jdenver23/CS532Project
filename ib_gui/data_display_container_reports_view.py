#!/usr/bin/python3
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from .tkentrycomplete import AutocompleteCombobox
from .utils import get_icon, tk_center, PatientAccount
from InsuranceBilling import InsuranceBilling, generate_delinquent_reports


class ReportsViewWidget(tk.Toplevel):
    def __init__(self, master=None, bill: InsuranceBilling=None, **kw):
        super(ReportsViewWidget, self).__init__(master, **kw)
        self.master = master
        self.bill = bill
        
        self.section_title = tk.Frame(self)
        self.section_title.configure(height=25, width=960)
        self.lb_title = tk.Label(self.section_title)
        self.lb_title.configure(
            font="{Verdana} 10 {bold}",
            text='Generate Delinquent Reports')
        self.lb_title.place(x=15)
        self.section_title.pack(anchor="w", padx=10, pady=10, side="top")
        self.section_title.pack_propagate(0)
        self.line_selector = tk.LabelFrame(self)
        self.line_selector.configure(height=2, width=235)
        self.line_selector.place(x=15, y=35)
        
        self.frame_carrier_sel = tk.Frame(self)
        self.frame_carrier_sel.configure(height=200, width=200)
        
        self.lb_carrier_name = tk.Label(self.frame_carrier_sel)
        self.lb_carrier_name.configure(
            font="{Verdana} 10 {}", text='Carrier name:')
        self.lb_carrier_name.pack(anchor="w", fill="x", padx=25, side="left")
        self.entry_carrier_name = tk.Entry(self.frame_carrier_sel)
        self.entry_carrier_name.configure(font="{Verdana} 8 {}", width=23)
        self.entry_carrier_name.pack(ipady=5, padx=15, side="left")
        self.lb_carrier_address = tk.Label(self.frame_carrier_sel)
        self.lb_carrier_address.configure(
            font="{Verdana} 10 {}", text='Carrier address:')
        self.lb_carrier_address.pack(anchor="w", fill="x", side="left")
        self.entry_carrier_address = tk.Entry(self.frame_carrier_sel)
        self.entry_carrier_address.configure(font="{Verdana} 8 {}", width=23)
        self.entry_carrier_address.pack(ipady=5, padx=15, side="left")
        
        self.btn_carrier_search = tk.Button(self.frame_carrier_sel)
        self.img_search = tk.PhotoImage(file=get_icon("search.png"))
        self.btn_carrier_search.configure(
            default="active",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            image=self.img_search,
            overrelief="groove",
            takefocus=True)
        self.btn_carrier_search.pack(anchor="n", side="left")
        self.btn_carrier_search.configure(command=self.carrier_search)
        self.frame_carrier_sel.pack(fill="x", padx=15, side="top")
        
        self.frame_or = tk.Frame(self)
        self.frame_or.configure(height=200, width=200)
        self.lb_or_line_top = tk.Label(self.frame_or)
        self.lb_or_line_top.configure(font="{Verdana} 8 {}", text='|')
        self.lb_or_line_top.pack(side="top")
        self.lb_or = tk.Label(self.frame_or)
        self.lb_or.configure(font="{Verdana} 13 {bold}", text='OR')
        self.lb_or.pack(side="top")
        self.lb_or_line_bot = tk.Label(self.frame_or)
        self.lb_or_line_bot.configure(font="{Verdana} 8 {}", text='|')
        self.lb_or_line_bot.pack(side="top")
        self.frame_or.pack(fill="x", side="top")
        
        self.frame_patient_sel = tk.Frame(self)
        self.frame_patient_sel.configure(height=200, width=200)
        self.sel_combo_frame = tk.Frame(self.frame_patient_sel)
        self.sel_combo_frame.configure(height=200, width=200)
        self.lb_patient_sel = tk.Label(self.sel_combo_frame)
        self.lb_patient_sel.configure(
            font="{Verdana} 10 {}",
            text='Select patient:')
        self.lb_patient_sel.pack(anchor="w", fill="x", padx=25, side="left")
        
        self.entry_patient_sel = AutocompleteCombobox(self.sel_combo_frame)
        self.entry_patient_sel.configure(width=75)
        self.entry_patient_sel.set_callback(self.autocompleteccb_patient)
        self.entry_patient_sel.bind("<<ComboboxSelected>>", self.autocompleteccb_patient)
        self.patient_account = PatientAccount()
        self.entry_patient_sel.set_completion_list(self.patient_account.as_description_list())
        self.entry_patient_sel.pack(anchor="w", ipady=5, padx=15, side="left")
        
        self.btn_patient_search = tk.Button(self.sel_combo_frame)
        self.btn_patient_search.configure(
            default="active",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            image=self.img_search,
            overrelief="groove",
            takefocus=True)
        self.btn_patient_search.pack(anchor="w", side="left")
        self.btn_patient_search.configure(command=self.patient_search)
        self.sel_combo_frame.pack(fill="x", padx=10, pady=5, side="top")
        
        self.frame_search_options = tk.Frame(self.frame_patient_sel)
        self.frame_search_options.configure(height=200, width=200)
        self.lb_search_filter = tk.Label(self.frame_search_options)
        self.lb_search_filter.configure(font="{Verdana} 10 {}", text='Filter:')
        self.lb_search_filter.pack(anchor="w", padx=25, side="left")
        
        self.radio_search_by_id = tk.Radiobutton(self.frame_search_options)
        self.search_filter = tk.IntVar(value=0)
        self.search_filter.trace_add("write", self.patient_search_filter_upd)
        self.radio_search_by_id.configure(
            padx=5,
            takefocus=True,
            text='ID',
            value=0,
            variable=self.search_filter)
        self.radio_search_by_id.pack(side="left")
        self.radio_search_by_name = tk.Radiobutton(self.frame_search_options)
        self.radio_search_by_name.configure(
            padx=5, text='Name', value=1, variable=self.search_filter)
        self.radio_search_by_name.pack(side="left")
        self.radio_search_by_email = tk.Radiobutton(self.frame_search_options)
        self.radio_search_by_email.configure(
            padx=5, text='Email', value=2, variable=self.search_filter)
        self.radio_search_by_email.pack(side="left")
        self.radio_search_by_dob = tk.Radiobutton(self.frame_search_options)
        self.radio_search_by_dob.configure(
            padx=5,
            text='Date of Birth',
            value=3,
            variable=self.search_filter)
        self.radio_search_by_dob.pack(side="left")
        self.radio_search_by_phone_number = tk.Radiobutton(
            self.frame_search_options)
        self.radio_search_by_phone_number.configure(
            padx=5, text='Phone Number', value=4, variable=self.search_filter)
        self.radio_search_by_phone_number.pack(side="left")
        self.frame_search_options.pack(pady=5, side="top")
        self.frame_patient_sel.pack(fill="x", side="top")
        
        self.frame_reports_info = tk.Frame(self)
        self.text_reports_info = ScrolledText(self.frame_reports_info, font="{Verdana} 10 {}", height=20)
        self.text_reports_info.configure(state=tk.DISABLED)
        self.text_reports_info.pack(padx=15, pady=10, ipadx=5, fill="both", side="top", expand=True)
        self.frame_reports_info.pack(fill="x", side="top")
        
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
        self.btn_back.pack(ipadx=5, ipady=5, side="top")
        self.btn_back.configure(command=self.form_cancel)
        self.control_container.pack(anchor="w", padx=15, pady=15, side="top")
        self.configure(takefocus=True)
        self.geometry("720x630")
        self.resizable(False, False)
        self.title("Generate Reports  - Healthcare Permanente")

        self.wm_protocol("WM_DELETE_WINDOW", self.on_closing)
        
        tk_center(self, gui_w=720, gui_h=630)
        self.ddc = self.master.calls(widget_name="ddc")
        
    def on_closing(self, event=None):
        self.destroy()
        self.ddc.toplevel_callback()
    
    def autocompleteccb_carrier(self, *args):
        self.carrier_search()
        
    def autocompleteccb_patient(self, *args):
        self.patient_search()
        
    def patient_search_filter_upd(self, *event):
        self.entry_patient_sel.delete(0, tk.END)
        if self.search_filter.get() == 0: # ID
            self.entry_patient_sel.set_completion_list(self.patient_account.as_description_list("ID"))
        elif self.search_filter.get() == 1: # Name
            self.entry_patient_sel.set_completion_list(self.patient_account.as_description_list("Name"))
        elif self.search_filter.get() == 2: # Email
            self.entry_patient_sel.set_completion_list(self.patient_account.as_description_list("Email"))
        elif self.search_filter.get() == 3: # DOB
            self.entry_patient_sel.set_completion_list(self.patient_account.as_description_list("DOB"))
        elif self.search_filter.get() == 4: # Phone#
            self.entry_patient_sel.set_completion_list(self.patient_account.as_description_list("Phone#"))
        
    def carrier_search(self):
        _name = self.entry_carrier_name.get()
        _address = self.entry_carrier_address.get()
        _info = generate_delinquent_reports(carrier_name=_name, carrier_address=_address)
        self.entry_info_upd(_info)
        
    def patient_search(self):
        if self.entry_patient_sel.get() in self.entry_patient_sel['values']:
            _id = self.entry_patient_sel.get().split(",")[self.search_filter.get()].strip()
            _info = generate_delinquent_reports(user_id=_id)
            self.entry_info_upd(_info)
        
    def entry_info_upd(self, text):
        self.text_reports_info.configure(state=tk.NORMAL)
        self.text_reports_info.delete("0.0", tk.END)
        self.text_reports_info.insert("0.0", text)
        self.text_reports_info.configure(state=tk.DISABLED)

    def form_cancel(self):
        self.destroy()
        self.ddc.toplevel_callback()


if __name__ == "__main__":
    root = tk.Tk()
    widget = ReportsViewWidget(root)
    # widget.pack(expand=True, fill="both")
    root.mainloop()
