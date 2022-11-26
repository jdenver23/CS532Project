#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox
from .tkentrycomplete import AutocompleteCombobox
from .utils import get_icon, tk_center, PatientAccount


class DataDisplayContainerPatientSelectWidget(tk.Toplevel):
    def __init__(self, master=None, **kw):
        super(DataDisplayContainerPatientSelectWidget,self).__init__(master,**kw)
        self.master = master
        
        self.section_title = tk.Frame(self)
        self.section_title.configure(height=25, width=960)
        self.lb_title = tk.Label(self.section_title)
        self.lb_title.configure(
            font="{Verdana} 10 {bold}",
            text='Select a Patient')
        self.lb_title.place(x=15)
        self.section_title.pack(anchor="w", padx=10, pady=10, side="top")
        self.section_title.pack_propagate(0)
        self.line_selector = tk.LabelFrame(self)
        self.line_selector.configure(height=2, width=140)
        self.line_selector.place(x=15, y=35)
        self.frame_patient_sel = tk.Frame(self)
        self.frame_patient_sel.configure(height=200, width=200)
        self.sel_combo_frame = tk.Frame(self.frame_patient_sel)
        self.sel_combo_frame.configure(height=200, width=200)
        self.lb_patient_sel = tk.Label(self.sel_combo_frame)
        self.lb_patient_sel.configure(
            font="{Verdana} 10 {}",
            text='Select patient:')
        self.lb_patient_sel.pack(anchor="w", padx=25, side="left")
        
        self.entry_patient_sel = AutocompleteCombobox(self.sel_combo_frame)
        self.entry_patient_sel.configure(width=75)
        self.entry_patient_sel.set_callback(self.autocomplete_ccb_keyhandle)
        self.entry_patient_sel.bind("<<ComboboxSelected>>", self.autocomplete_ccb_keyhandle)
        self.patient_account = PatientAccount()
        self.entry_patient_sel.set_completion_list(self.patient_account.as_description_list())
        self.entry_patient_sel.pack(anchor="w", ipady=5, padx=15, side="left")
        
        self.btn_search = tk.Button(self.sel_combo_frame)
        self.img_search = tk.PhotoImage(file=get_icon("search.png"))
        self.btn_search.configure(
            default="active",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            image=self.img_search,
            overrelief="groove",
            takefocus=True)
        self.btn_search.pack(anchor="w", side="left")
        self.btn_search.configure(command=self.patient_search)
        self.sel_combo_frame.pack(padx=10, pady=5, side="top")
        
        self.frame_search_options = tk.Frame(self.frame_patient_sel)
        self.frame_search_options.configure(height=200, width=200)
        self.lb_search_filter = tk.Label(self.frame_search_options)
        self.lb_search_filter.configure(font="{Verdana} 10 {}", text='Filter:')
        self.lb_search_filter.pack(anchor="w", padx=25, side="left")
        
        self.radio_search_by_id = tk.Radiobutton(self.frame_search_options)
        self.search_filter = tk.IntVar(value=0)
        self.search_filter.trace_add("write", self.search_filter_upd)
        self.radio_search_by_id.configure(
            padx=5, takefocus=True, text='ID', value=0, variable=self.search_filter)
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
            padx=5, text='Date of Birth', value=3, variable=self.search_filter)
        self.radio_search_by_dob.pack(side="left")
        self.radio_search_by_phone_number = tk.Radiobutton(self.frame_search_options)
        self.radio_search_by_phone_number.configure(
            padx=5, text='Phone Number', value=4, variable=self.search_filter)
        self.radio_search_by_phone_number.pack(side="left")
        self.frame_search_options.pack(pady=5, side="top")
        self.frame_patient_sel.pack(fill="x", side="top")
        
        self.line_seperator_0 = tk.LabelFrame(self)
        self.line_seperator_0.configure(height=2, width=140)
        self.line_seperator_0.pack(fill="x", padx=15, pady=5, side="top")
        
        self.frame_patient_info = tk.Frame(self)
        self.frame_patient_info.configure(height=200, width=200)
        self.form_frame = tk.Frame(self.frame_patient_info)
        self.form_frame.configure(height=200, width=200)
        self.form_frame_r1 = tk.Frame(self.form_frame)
        self.form_frame_r1.configure(height=200, width=200)
        self.frame_name = tk.Frame(self.form_frame_r1)
        self.frame_name.configure(height=200, width=200)
        self.lb_patient_name = tk.Label(self.frame_name)
        self.lb_patient_name.configure(
            font="{Verdana} 8 {}", text='First, Last:', width=20)
        self.lb_patient_name.pack(anchor="e", side="left")
        self.entry_patient_name = tk.Entry(self.frame_name)
        self.entry_patient_name.configure(
            font="{Verdana} 9 {}",
            justify="left",
            state="disabled",
            width=20)
        self.entry_patient_name.pack(ipady=5, side="left")
        self.frame_name.pack(anchor="w", side="left")
        self.frame_email = tk.Frame(self.form_frame_r1)
        self.frame_email.configure(height=200, width=200)
        self.lb_patient_email = tk.Label(self.frame_email)
        self.lb_patient_email.configure(
            font="{Verdana} 8 {}", text='Email:', width=20)
        self.lb_patient_email.pack(anchor="e", side="left")
        self.entry_patient_email = tk.Entry(self.frame_email)
        self.entry_patient_email.configure(
            font="{Verdana} 9 {}",
            justify="left",
            state="disabled",
            width=20)
        self.entry_patient_email.pack(ipady=5, side="top")
        self.frame_email.pack(anchor="w", pady=20, side="left")
        self.form_frame_r1.pack(fill="x", side="top")
        self.form_frame_r2 = tk.Frame(self.form_frame)
        self.form_frame_r2.configure(height=200, width=200)
        self.frame_dob = tk.Frame(self.form_frame_r2)
        self.frame_dob.configure(height=200, width=200)
        self.lb_patient_dob = tk.Label(self.frame_dob)
        self.lb_patient_dob.configure(
            font="{Verdana} 8 {}",
            text='Date of Birth:',
            width=20)
        self.lb_patient_dob.pack(anchor="e", side="left")
        self.entry_patient_dob = tk.Entry(self.frame_dob)
        self.entry_patient_dob.configure(
            font="{Verdana} 9 {}",
            justify="center",
            state="disabled",
            width=10)
        self.entry_patient_dob.pack(ipady=5, side="top")
        self.frame_dob.pack(anchor="w", fill="x", side="left")
        self.frame_gender = tk.Frame(self.form_frame_r2)
        self.frame_gender.configure(height=200, width=200)
        self.lb_patient_gender = tk.Label(self.frame_gender)
        self.lb_patient_gender.configure(
            font="{Verdana} 8 {}", text='Gender:', width=16)
        self.lb_patient_gender.pack(anchor="e", side="left")
        self.entry_patient_gender = tk.Entry(self.frame_gender)
        self.entry_patient_gender.configure(
            font="{Verdana} 8 {}",
            justify="center",
            state="disabled",
            width=7)
        self.entry_patient_gender.pack(ipady=5, side="top")
        self.frame_gender.pack(anchor="w", fill="x", side="left")
        self.frame_phone_number = tk.Frame(self.form_frame_r2)
        self.frame_phone_number.configure(height=200, width=200)
        self.lb_patient_phone_number = tk.Label(self.frame_phone_number)
        self.lb_patient_phone_number.configure(
            font="{Verdana} 8 {}", text='Phone #:', width=16)
        self.lb_patient_phone_number.pack(anchor="e", side="left")
        self.entry_patient_phone_number = tk.Entry(self.frame_phone_number)
        self.entry_patient_phone_number.configure(
            font="{Verdana} 9 {}", justify="center", state="disabled", width=12)
        self.entry_patient_phone_number.pack(ipady=5, side="top")
        self.frame_phone_number.pack(
            anchor="e", fill="x", pady=20, side="left")
        self.form_frame_r2.pack(fill="x", side="top")
        self.form_frame_r3 = tk.Frame(self.form_frame)
        self.form_frame_r3.configure(height=200, width=200)
        self.frame2 = tk.Frame(self.form_frame_r3)
        self.frame2.configure(height=200, width=200)
        self.lb_patient_address = tk.Label(self.frame2)
        self.lb_patient_address.configure(
            font="{Verdana} 8 {}", text='Address:', width=20)
        self.lb_patient_address.pack(anchor="e", side="left")
        self.entry_patient_address = tk.Entry(self.frame2)
        self.entry_patient_address.configure(
            font="{Verdana} 9 {}",
            justify="left",
            state="disabled",
            width=59)
        self.entry_patient_address.pack(fill="x", ipady=5, side="top")
        self.frame2.pack(anchor="w", fill="x", side="left")
        self.form_frame_r3.pack(fill="x", ipady=10, side="top")
        self.form_frame.pack(fill="x", padx=15, side="top")
        self.frame_patient_info.pack(fill="x", side="top")
        
        self.control_container = tk.Frame(self)
        self.btn_select = tk.Button(self.control_container)
        self.btn_select.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            overrelief="ridge",
            takefocus=True,
            text='Select ✓')
        self.btn_select.pack(ipadx=5, ipady=5, side="right")
        self.btn_select.configure(command=self.form_submit)
        self.btn_back = tk.Button(self.control_container)
        self.btn_back.configure(
            background="#2980b9",
            disabledforeground="black",
            font="{Verdana} 10 {}",
            foreground="white",
            justify="left",
            overrelief="ridge",
            text='⬅ Back')
        self.btn_back.pack(ipadx=5, ipady=5, padx=10, side="right")
        self.btn_back.configure(command=self.form_cancel)
        self.control_container.pack(fill="x", padx=30, pady=15, side="bottom")
        
        self.configure(takefocus=True, width=200)
        self.geometry("720x390")
        self.resizable(False, False)
        self.title("Select a Patient - Healthcare Permanente")
        
        self.wm_protocol("WM_DELETE_WINDOW", self.on_closing)
        
        tk_center(self, gui_h=390, gui_w=720)
        self.nbc = self.master.calls(widget_name="nbc")
        
    def on_closing(self, event=None):
        if messagebox.askyesno("Patient Select", "Are you sure you want to close this window? This will log you out of the system."):
            self.destroy()
            self.nbc.logout(forced=True)
    
    def autocomplete_ccb_keyhandle(self, *args):
        self.patient_search()
        
    def search_filter_upd(self, *event):
        self.clear_entries()
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
        
    def patient_search(self):
        _id = self.entry_patient_sel.get().split(",")[self.search_filter.get()].strip()
        patient = self.patient_account.get_patient(_id)
        self.clear_entries()
        if patient is None: 
            return
        
        self.entry_patient_name.configure(state=tk.NORMAL)
        self.entry_patient_email.configure(state=tk.NORMAL)
        self.entry_patient_dob.configure(state=tk.NORMAL)
        self.entry_patient_gender.configure(state=tk.NORMAL)
        self.entry_patient_phone_number.configure(state=tk.NORMAL)
        self.entry_patient_address.configure(state=tk.NORMAL)
        
        self.entry_patient_name.insert(0, patient.name)
        self.entry_patient_email.insert(0, patient.email)
        self.entry_patient_dob.insert(0, patient.dob)
        self.entry_patient_gender.insert(0, patient.gender)
        self.entry_patient_phone_number.insert(0, patient.phone_number)
        self.entry_patient_address.insert(0, patient.address)
        
        self.entry_patient_name.configure(state=tk.DISABLED)
        self.entry_patient_email.configure(state=tk.DISABLED)
        self.entry_patient_dob.configure(state=tk.DISABLED)
        self.entry_patient_gender.configure(state=tk.DISABLED)
        self.entry_patient_phone_number.configure(state=tk.DISABLED)
        self.entry_patient_address.configure(state=tk.DISABLED)

    def clear_entries(self):
        self.entry_patient_name.configure(state=tk.NORMAL)
        self.entry_patient_email.configure(state=tk.NORMAL)
        self.entry_patient_dob.configure(state=tk.NORMAL)
        self.entry_patient_gender.configure(state=tk.NORMAL)
        self.entry_patient_phone_number.configure(state=tk.NORMAL)
        self.entry_patient_address.configure(state=tk.NORMAL)
        
        self.entry_patient_name.delete(0, tk.END)
        self.entry_patient_email.delete(0, tk.END)
        self.entry_patient_dob.delete(0, tk.END)
        self.entry_patient_gender.delete(0, tk.END)
        self.entry_patient_phone_number.delete(0, tk.END)
        self.entry_patient_address.delete(0, tk.END)
        
        self.entry_patient_name.configure(state=tk.DISABLED)
        self.entry_patient_email.configure(state=tk.DISABLED)
        self.entry_patient_dob.configure(state=tk.DISABLED)
        self.entry_patient_gender.configure(state=tk.DISABLED)
        self.entry_patient_phone_number.configure(state=tk.DISABLED)
        self.entry_patient_address.configure(state=tk.DISABLED)

    def form_submit(self):
        _id = self.entry_patient_sel.get().split(",")[self.search_filter.get()].strip()
        patient = self.patient_account.get_patient(_id)
        if patient is None:
            messagebox.showerror("Error", "Could not process last request (error while retrieving patient info). Please try again.")
            self.focus_force()
            return
        
        self.destroy()
        self.nbc.toplevel_callback(patient)

    def form_cancel(self):
        self.destroy()
        self.nbc.toplevel_callback()


if __name__ == "__main__":
    root = tk.Tk()
    widget = DataDisplayContainerPatientSelectWidget(root)
    # widget.pack(expand=True, fill="both")
    root.mainloop()
