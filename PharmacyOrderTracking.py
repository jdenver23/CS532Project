#-----------------------------------------------------
# CS 532 Software Engineering
# Class Project - Healthcare 
# 
# Author: Jonathan Lee
# PharmacyOrderTracking.py
#
# Class to keep track of and execute necessary actions
# related to Pharmacy Orders. 
#
# https://www.tutorialspoint.com/how-to-display-a-listbox-with-columns-using-tkinter
# https://www.pythontutorial.net/tkinter/tkinter-theme/
# https://www.pythontutorial.net/tkinter/tkinter-treeview/
# https://www.tutorialspoint.com/how-to-change-ttk-treeview-column-width-and-weight-in-python-3-3
# https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
# https://stackoverflow.com/questions/68148391/placing-multiple-buttons-in-same-column-tkinter-using-grid
# https://www.youtube.com/watch?v=yICGS9Lv86s - used to help find if multiple rows in TreeView selected.
# https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/blob/master/treebase.py - for Search
# https://www.youtube.com/watch?v=odt87CeLlro
# https://www.youtube.com/watch?v=rtR5wHXPKZ4&list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV&index=117
# https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course
# https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/blob/master/tree.py
# https://www.geeksforgeeks.org/scrollable-listbox-in-python-tkinter/
#-----------------------------------------------------

import PharmacyOrder as PO
import Medications as MED
# import CompleteOrder 
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import csv

PRESC_ID_LOC = 0
PAT_NAME_LOC = 1
PAT_ID_LOC = 2 
PHYS_NAME_LOC = 3
PRESC_MED_LOC = 4
MED_ID_LOC = 5
DOSAGE_LOC = 6
FREQ_LOC = 7
D_ORD_LOC= 8
D_FILL_LOC = 9
PHARM_LOC = 10

USERS_CSV = "users.csv"
USERS_FIELD_NAMES = ['ID', 'First Name', 'Last Name', 'Email,Password', 'Phone Number', 'Address', 'Insurance Carrier', 'Date of Birth', 'Gender', 'Primary Care Physician', 'Medication' , 'Appointments']

class PharmacyOrderTracking:
    
    def __init__(self, user_ID):
        self.pharm_order_accessor = PO.PharmacyOrder()
        self.medication_accessor = MED.Medications()
        self.user_ID = user_ID
        pass
    
    def PO_add_order(self, user_id, prescription_id, patient_name, patient_id, physician_name, medication, medication_id, dosage, medication_frequency, date_ordered, date_filled, pharmacist):
        self.pharm_order_accessor.add_order(user_id, prescription_id, patient_name, patient_id, physician_name, medication, medication_id, dosage, medication_frequency, date_ordered, date_filled, pharmacist)
    
    def PO_delete_pharmacy_order(self, user_id, presc_ID):
        self.pharm_order_accessor.delete_pharmacy_order(user_id, presc_ID)
    
    # might not be needed. 
    def PO_print_prescriptions(self, p_list):
        self.pharm_order_accessor.print_prescriptions(p_list)
    
    # GUI Done
    def PO_prescriptions_ordered_by_physician_list(self, user_id, physician_name, start_time, end_time):
        return self.pharm_order_accessor.prescriptions_ordered_by_physician_list(user_id, physician_name, start_time, end_time)
    
    # GUI done
    def PO_prescriptions_filled_for_patient_list(self, user_id, patient_name, start_time, end_time):
        return self.pharm_order_accessor.prescriptions_filled_for_patient_list(user_id, patient_name, start_time, end_time)
    
    # GUI DONE
    def PO_report_num_presc_by_medication_month_physician_list(self, user_id):
        return self.pharm_order_accessor.report_num_presc_by_medication_month_physician_list(user_id)
    
    # NOT needed
    def PO_report_num_presc_by_medication_month_physician(self, dict_result):
        self.pharm_order_accessor.report_num_presc_by_medication_month_physician(dict_result)
    
    # NOT needed
    def PO_print_search_by_prescription_id(self, dict_info, p_ID):
        self.pharm_order_accessor.print_search_by_prescription_id(dict_info, p_ID)
    
    # GUI Done
    def PO_search_by_prescription_id_list(self, user_id, prescription_id):
        return self.pharm_order_accessor.search_by_prescription_id_list(user_id, prescription_id)

    # MIGHT NOT BE NEEDED.
    def PO_print_search_by_patient_name_and_medication(self, list_info, p_name, med):
        self.pharm_order_accessor.print_search_by_patient_name_and_medication(list_info, p_name, med)
    
    # GUI done
    def PO_search_by_patient_name_and_medication_list(self, user_id, patient_name, prescribed_medication):
        return self.pharm_order_accessor.search_by_patient_name_and_medication_list(user_id, patient_name, prescribed_medication)
    
    def PO_orders_to_be_filled(self, user_id):
        return self.pharm_order_accessor.orders_to_be_filled(user_id)
    
    def PO_orders_to_be_filled(self, user_id):
        return self.pharm_order_accessor.orders_filled(user_id)

    # GUI done
    def PO_show_prescription_orders_list(self, user_id):
        return self.pharm_order_accessor.show_prescription_orders_list(user_id)
    
    # GUI done
    def PO_complete_order(self, user_id, presc_ID, pharmacist_name, date_filled):
        return self.pharm_order_accessor.complete_order(user_id, presc_ID, pharmacist_name, date_filled)


# get_patient_name takes a user Id and returns the user's full name from information gathere
# from users.csv database.
# user_ID: string
def get_patient_name(user_ID):
    with open(USERS_CSV, mode='r', newline='') as f:
        reader = csv.DictReader(f, fieldnames=USERS_FIELD_NAMES)
        for row in reader: 
            if row["ID"] == user_ID:
                return row["First Name"] + " " + row["Last Name"]
        
        return ""


# GUI driven with tkinter
def runGUI(POT_var):
    root = tk.Tk()
    
    root.title("Pharmacy Order Tracking")

    top = Frame(root)
    bottom = Frame(root)
    # top.pack(side=TOP)
    # bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
    top.grid(row=0, column=0, sticky='ns')
    bottom.grid(row=1, column=0, sticky='ns')

    root.geometry("1275x700")

    # define columns
    PO_columns = ("Prescription_ID","Patient_Name","Patient_ID","Physician_Name","Prescribed_Medication","Medication_ID","Dosage","Frequency","Date_Ordered","Date_Filled","Pharmacist")

    tree = ttk.Treeview(bottom, columns=PO_columns, show='headings')

    # define headings and columns
    tree.column("Prescription_ID", anchor=CENTER, stretch=YES, width=90)
    tree.heading('Prescription_ID', text="Prescription ID")
    tree.column("Patient_Name", anchor=CENTER, stretch=YES, width=150)
    tree.heading('Patient_Name', text="Patient Name")
    tree.column("Patient_ID", anchor=CENTER, stretch=YES, width=90)
    tree.heading('Patient_ID', text="Patient ID")
    tree.column("Physician_Name", anchor=CENTER, stretch=YES, width=150)
    tree.heading('Physician_Name', text="Physician Name")
    tree.column("Prescribed_Medication", anchor=CENTER, stretch=YES, width=150)
    tree.heading('Prescribed_Medication', text="Prescribed Medication")
    tree.column("Medication_ID", anchor=CENTER, stretch=YES, width=100)
    tree.heading('Medication_ID', text="Medication ID")
    tree.column("Dosage", anchor=CENTER, stretch=YES, width=80)
    tree.heading('Dosage', text="Dosage")
    tree.column("Frequency", anchor=CENTER, stretch=YES, width=150)
    tree.heading('Frequency', text="Frequency")
    tree.column("Date_Ordered", anchor=CENTER, stretch=YES, width=80)
    tree.heading('Date_Ordered', text="Date Ordered")
    tree.column("Date_Filled", anchor=CENTER, stretch=YES, width=70)
    tree.heading('Date_Filled', text="Date Filled")
    tree.column("Pharmacist", anchor=CENTER, stretch=YES, width=150)
    tree.heading('Pharmacist', text="Pharmacist")
    
    PO_list = POT_var.PO_show_prescription_orders_list(POT_var.user_ID)

    for order in PO_list:
        tree.insert('', tk.END, values=order)

    tree.grid(row=1, column=0, sticky='nsew')

    scrollbar_vert = ttk.Scrollbar(bottom, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar_vert.set)
    # TODO: needs to be fixed. 
    scrollbar_vert.grid(row=1, column=1, sticky='ns')

    scrollbar_hor = ttk.Scrollbar(bottom, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(xscroll=scrollbar_hor.set)
    # TODO: needs to be fixed
    scrollbar_hor.grid(row=2, column=0, sticky='ns')

    # NOW add HOME option on top toolbar.
    def return_home():
        root.destroy()
        return

    home_button = ttk.Button(top, text='Home', command = return_home)
    # home_button.pack(in_=top, side=LEFT)
    home_button.grid(row=0, column=1, sticky='ew')


    # NOW add COMPLETE ORDER option to top toolbar
    def complete_order():
        # multiple_selection is only used to make sure that only one row is selected
        multiple_selection = tree.selection()
        if len(multiple_selection) == 0:
            # TODO: needs to be changed later
            print("ERROR: Must select an order before clicking Complete Order")
            return
        elif len(multiple_selection) >= 2:
            # TODO: needs to be changed later
            print("ERROR: Only one order can be completed at a time.")
            return
        else:
            selected = tree.focus()
            # NOTE: not sure what "values" does
            selected_list = tree.item(selected, "values")
            CO_run_GUI(POT_var.user_ID, selected_list, POT_var, root)
        
        root.destroy()

    user_ID_int = int(POT_var.user_ID)
    if user_ID_int >= 30000000 and user_ID_int < 40000000:
        complete_order_button = ttk.Button(top, text='Complete Selected Order', command = complete_order)
        # edit_button.pack(in_=top, side=LEFT)
        complete_order_button.grid(row=1, column=2, sticky='w')
    
    def add_order():
        add_order_run_GUI(POT_var.user_ID, POT_var, root)

    if user_ID_int >= 30000000 and user_ID_int < 40000000:
        add_order_button = ttk.Button(top, text='Add New Order', command = add_order)
        # edit_button.pack(in_=top, side=LEFT)
        add_order_button.grid(row=1, column=0, sticky='w')

    def close_delete_window():
        delete_order_confirmation.destroy()

    def delete_action():
        delete_order_confirmation.destroy()

        POT_var.PO_delete_pharmacy_order(POT_var.user_ID, to_be_deleted_presc_id)

        # clear Tree view
        for order in tree.get_children():
            tree.delete(order)

        # get updated prescription list
        PO_list_updated = POT_var.PO_show_prescription_orders_list(POT_var.user_ID)

        # insert them back to the treeview
        for order in PO_list_updated:
            tree.insert('', tk.END, values=order)

    
    def delete_order_confirmation_GUI(sel_list):
        global delete_order_confirmation, to_be_deleted_presc_id
        delete_order_confirmation = Toplevel(root)
        delete_order_confirmation.title("Delete Order Confirmation")
        delete_order_confirmation.geometry("400x200")

        to_be_deleted_presc_id = sel_list[0]

        label = Label(delete_order_confirmation, text="Are you sure you want to delete Pharmacy Order with ID #"+sel_list[0]+"?")
        label.pack(padx=10, pady=10)

        # presc_ID_frame =LabelFrame(delete_order_confirmation, text="Prescription ID")
        # presc_ID_frame.pack(padx=10, pady=10)

        # presc_ID_entry = Entry(presc_ID_frame, font=("Helvetica", 10))
        # presc_ID_entry.pack(pady=20, padx=20)

        Yes_button = Button(delete_order_confirmation, text="YES, I want to Delete", command=delete_action)
        Yes_button.pack(padx=5, pady=5)

        No_button = Button(delete_order_confirmation, text="NO, this was a mistake", command=close_delete_window)
        No_button.pack(padx=5, pady=5)
        pass    

    def delete_order():
        # multiple_selection is only used to make sure that only one row is selected
        multiple_selection = tree.selection()
        if len(multiple_selection) == 0:
            # TODO: needs to be changed later
            print("ERROR: Must select an order before clicking Delete Order")
            return
        elif len(multiple_selection) >= 2:
            # TODO: needs to be changed later
            print("ERROR: Only one order can be deleted at a time.")
            return
        else:
            selected = tree.focus()
            # NOTE: not sure what "values" does
            selected_list = tree.item(selected, "values")
            delete_order_confirmation_GUI(selected_list)
        
        # root.destroy()

    if user_ID_int >= 30000000 and user_ID_int < 40000000:
        delete_order_button = ttk.Button(top, text='Delete Selected Order', command = delete_order)
        # edit_button.pack(in_=top, side=LEFT)
        delete_order_button.grid(row=1, column=1, sticky='w')

    
    # NOW add MENU option to root.
    POT_menu = Menu(root)
    root.config(menu=POT_menu)

    # function execute the search button in the "Search by Prescription Name and Prescribed Medication"
    def execute_search_by_name_and_medication():
        patient_name_entered = patient_name_entry.get()
        medication_entered = medication_entry.get()

        # need to get rid of leading/trailing spaces. 
        patient_name_entered = patient_name_entered.strip()
        medication_entered = medication_entered.strip()

        # close the search option box
        search_BNAM.destroy()

        # clear Tree view
        for order in tree.get_children():
            tree.delete(order)
        
        # get resulting list from search. 
        search_result_list = POT_var.PO_search_by_patient_name_and_medication_list(POT_var.user_ID, patient_name_entered, medication_entered)

        for order in search_result_list:
            tree.insert('', tk.END, values=order)

    # TODO: needs a back button as well as a note to alert user that both entries must be filled. Also needs error messages.
    def search_by_name_and_medication():
        global search_BNAM, patient_name_entry, medication_entry

        search_BNAM = Toplevel(root)
        search_BNAM.title("Search By Patient Name & Prescribed Medication")
        search_BNAM.geometry("400x300")

        patient_name_frame = LabelFrame(search_BNAM, text="Patient Name")
        patient_name_frame.pack(padx=10, pady=10)

        patient_name_entry = Entry(patient_name_frame, font=("Helvetica", 10))
        if user_ID_int >= 40000000:
            # if the user is a patient, then only allow for their name to be an option 
            # (i.e. the user can't access other people's records. )
            patient_name_entry = Entry(patient_name_frame)
            # default the Entry box to have the patient's name
            patient_name_entry.insert(0, get_patient_name(POT_var.user_ID))
            # make the textbox read-only so that the user can't change the name. 
            patient_name_entry.config(state='readonly')
        patient_name_entry.pack(pady=20, padx=20)

        medication_frame = LabelFrame(search_BNAM, text="Prescribed Medication")
        medication_frame.pack(padx=10, pady=10)

        medication_entry = Entry(medication_frame, font=("Helvetica", 10))
        medication_entry.pack(pady=20, padx=20)

        search_BNAM_button = Button(search_BNAM, text="Search Orders", command=execute_search_by_name_and_medication)
        search_BNAM_button.pack(padx=20, pady=20)

    # TODO: still needs a back button as well as alert user that entry must be filled. also needs error messages. 
    def execute_search_by_presc_id():
        presc_ID_entered = presc_ID_entry.get()

        # need to get rid of leading/trailing spaces.
        presc_ID_entered = presc_ID_entered.strip()

        # close the search option box
        search_BPI.destroy()

        # clear Treeview
        for order in tree.get_children():
            tree.delete(order)
        
        # get resulting list from search.
        search_result_list = POT_var.PO_search_by_prescription_id_list(POT_var.user_ID, presc_ID_entered)
        
        tree.insert('', tk.END, values=search_result_list)

    def search_by_presc_id():
        global presc_ID_entry, search_BPI
        search_BPI = Toplevel(root)
        search_BPI.title("Search By Prescription ID")
        search_BPI.geometry("400x200")

        presc_ID_frame =LabelFrame(search_BPI, text="Prescription ID")
        presc_ID_frame.pack(padx=10, pady=10)

        presc_ID_entry = Entry(presc_ID_frame, font=("Helvetica", 10))
        presc_ID_entry.pack(pady=20, padx=20)

        search_BPI_button = Button(search_BPI, text="Search Orders", command=execute_search_by_presc_id)
        search_BPI_button.pack(padx=20, pady=20)
        pass

    def reset_search():
        # clear Treeview
        for order in tree.get_children():
            tree.delete(order)

        full_list = POT_var.PO_show_prescription_orders_list(POT_var.user_ID)

        for order in full_list:
            tree.insert('', tk.END, values=order)


    def report_prescriptions_filled_for_patient():
        patient_name_entered = patient_name_entry.get()
        start_date_entered = start_date_entry_patient.get()
        end_date_entered = end_date_entry_patient.get()

        # get rid of leading/trailing Spaces
        patient_name_entered = patient_name_entered.strip()
        start_date_entered = start_date_entered.strip()
        end_date_entered = end_date_entered.strip()

        # clear the search option box.
        presc_patient.destroy()

        # clear Tree view
        for order in tree.get_children():
            tree.delete(order)
        
        report_list = POT_var.PO_prescriptions_filled_for_patient_list(POT_var.user_ID, patient_name_entered, start_date_entered, end_date_entered)

        for order in report_list:
            tree.insert('', tk.END, values=order)


    def prescriptions_filled_for_patient():
        global presc_patient, patient_name_entry, start_date_entry_patient, end_date_entry_patient
        presc_patient = Toplevel(root)
        presc_patient.title("Prescriptions Filled For a Patient")
        presc_patient.geometry("400x400")

        label = Label(presc_patient, text="List of All Prescriptions FILLED For a Patient For a Specific Period of Time")
        label.pack(padx=10, pady=10)
        
        patient_name_frame = LabelFrame(presc_patient, text="Patient Name")
        patient_name_frame.pack(padx=10, pady=10)

        patient_name_entry = Entry(patient_name_frame, font=("Helvetica", 10))
        if user_ID_int >= 40000000:
            # if the user is a patient, then only allow for their name to be an option 
            # (i.e. the user can't access other people's records. )
            patient_name_entry = Entry(patient_name_frame)
            # default the Entry box to have the patient's name
            patient_name_entry.insert(0, get_patient_name(POT_var.user_ID))
            # make the textbox read-only so that the user can't change the name. 
            patient_name_entry.config(state='readonly')
        patient_name_entry.pack(pady=20, padx=20)

        start_date_frame = LabelFrame(presc_patient, text="Start Date (MM/DD/YYYY)")
        start_date_frame.pack(padx=10, pady=10)

        start_date_entry_patient = Entry(start_date_frame, font=("Helvetica", 10))
        start_date_entry_patient.pack(pady=20, padx=20)

        end_date_frame = LabelFrame(presc_patient, text="End Date (MM/DD/YYYY)")
        end_date_frame.pack(padx=10, pady=10)

        end_date_entry_patient = Entry(end_date_frame, font=("Helvetica", 10))
        end_date_entry_patient.pack(pady=20, padx=20)

        report_prescriptions_filled_for_patient_button = Button(presc_patient, text="Create Report", command=report_prescriptions_filled_for_patient)
        report_prescriptions_filled_for_patient_button.pack(padx=20, pady=20)

    def report_prescriptions_ordered_by_physician():
        physician_name_entered = physician_name_entry.get()
        start_date_entered = start_date_entry_physician.get()
        end_date_entered = end_date_entry_physician.get()

        # get rid of leading/trailing Spaces
        physician_name_entered = physician_name_entered.strip()
        start_date_entered = start_date_entered.strip()
        end_date_entered = end_date_entered.strip()

        # clear the search option box.
        presc_physician.destroy()

        # clear Tree view
        for order in tree.get_children():
            tree.delete(order)
        
        report_list = POT_var.PO_prescriptions_ordered_by_physician_list(POT_var.user_ID, physician_name_entered, start_date_entered, end_date_entered)

        for order in report_list:
            tree.insert('', tk.END, values=order)

    def prescriptions_ordered_by_a_physician(): 
        global presc_physician, physician_name_entry, start_date_entry_physician, end_date_entry_physician        
        presc_physician = Toplevel(root)
        presc_physician.title("Prescriptions Ordered By a Physician")
        presc_physician.geometry("425x400")

        label = Label(presc_physician, text="List of All Prescriptions ORDERED By a Physician For a Specific Period of Time")
        label.pack(padx=10, pady=10)        

        physician_name_frame = LabelFrame(presc_physician, text="Physician Name")
        physician_name_frame.pack(padx=10, pady=10)

        physician_name_entry = Entry(physician_name_frame, font=("Helvetica", 10))
        physician_name_entry.pack(pady=20, padx=20)

        start_date_frame = LabelFrame(presc_physician, text="Start Date (MM/DD/YYYY)")
        start_date_frame.pack(padx=10, pady=10)

        start_date_entry_physician = Entry(start_date_frame, font=("Helvetica", 10))
        start_date_entry_physician.pack(pady=20, padx=20)

        end_date_frame = LabelFrame(presc_physician, text="End Date (MM/DD/YYYY)")
        end_date_frame.pack(padx=10, pady=10)

        end_date_entry_physician = Entry(end_date_frame, font=("Helvetica", 10))
        end_date_entry_physician.pack(pady=20, padx=20)

        report_prescriptions_filled_for_physician_button = Button(presc_physician, text="Create Report", command=report_prescriptions_ordered_by_physician)
        report_prescriptions_filled_for_physician_button.pack(padx=20, pady=20)

    def summary_report():
        report = Toplevel(root)
        report.title("Summary Report")
        report.geometry("450x400")

        listbox = Listbox(report, width=70)
        listbox.pack(side = LEFT, fill = BOTH)
        scrollbar =Scrollbar(report)
        scrollbar.pack(side=RIGHT, fill=BOTH)

        report_result_list = POT_var.PO_report_num_presc_by_medication_month_physician_list(POT_var.user_ID)

        for single_line in report_result_list:
            listbox.insert(END, single_line)

        listbox.config(yscrollcommand=scrollbar.set)

        scrollbar.config(command=listbox.yview)

        report.mainloop()

    # Add SEARCH menu options.
    search_menu_options = Menu(POT_menu, tearoff=0)
    POT_menu.add_cascade(label="Search", menu=search_menu_options)

    search_menu_options.add_command(label="Search By Patient Name & Medication", command=search_by_name_and_medication)
    search_menu_options.add_separator()
    search_menu_options.add_command(label="Search By Prescription ID", command=search_by_presc_id)
    search_menu_options.add_separator()
    search_menu_options.add_command(label="Reset Search", command=reset_search)

    # Add REPORTS menu opetions
    report_menu_options = Menu(POT_menu, tearoff=0)
    POT_menu.add_cascade(label="Reports", menu=report_menu_options)
    
    report_menu_options.add_command(label="Prescriptions Filled For a Patient", command=prescriptions_filled_for_patient)
    report_menu_options.add_separator()
    report_menu_options.add_command(label="Prescriptions Ordered By a Physician", command=prescriptions_ordered_by_a_physician)
    if int(POT_var.user_ID) >= 30000000 and int(POT_var.user_ID) < 40000000:
        report_menu_options.add_separator()
        report_menu_options.add_command(label="Summary Report", command=summary_report)
    report_menu_options.add_separator()
    report_menu_options.add_command(label="Reset Report", command=reset_search)

    root.mainloop()

# Iniital entry
def initialize(passed_user_id):
    # create Pharmacy Order Tracking (POT) instance with provided user ID. 
    POT_instance = PharmacyOrderTracking(passed_user_id)
    runGUI(POT_instance)


def add_order_run_GUI(passed_user_id, POT_var, root_window):
    AO_root = tk.Tk()
    AO_root.title("Add New Pharmacy Order")

    AO_root.geometry("400x350")

    def exit_entry():
        AO_root.destroy()
        root_window.destroy()
        initialize(passed_user_id)

    exit_button = tk.Button(AO_root, text='Back', command = exit_entry)
    exit_button.grid(row = 0, column = 0, pady = 5)

    prescription_id_var = tk.StringVar()
    patient_name_var = tk.StringVar()
    patient_id_var = tk.StringVar()
    physician_name_var = tk.StringVar()
    prescribed_med_var = tk.StringVar()
    medication_id_var = tk.StringVar()
    dosage_var = tk.StringVar()
    frequency_med_var = tk.StringVar()
    date_ordered_var = tk.StringVar()
    date_filled_var = tk.StringVar()
    pharmacist_var = tk.StringVar()


    def add_new_order():
        POT_var.PO_add_order(passed_user_id, presc_ID_entry.get(), patient_name_entry.get(), patient_ID_entry.get(), physician_name_entry.get(), presc_med_entry.get(), med_ID_entry.get(), dosage_entry.get(), freq_entry.get(), date_ordered_entry.get(), date_filled_entry.get(), pharmacist_entry.get())
        AO_root.destroy()
        root_window.destroy()
        initialize(passed_user_id)
    
    presc_ID_label = tk.Label(AO_root, text = "Prescription ID: ", font=('calibre',10, 'bold'))
    presc_ID_entry = tk.Entry(AO_root, textvariable=prescription_id_var, font=('calibre',10,'normal'))
    patient_name_label = tk.Label(AO_root, text = "Patient Name: ", font=('calibre',10, 'bold'))
    patient_name_entry = tk.Entry(AO_root, textvariable=patient_name_var, font=('calibre',10,'normal'))
    patient_ID_label = tk.Label(AO_root, text = "Patient ID: ", font=('calibre',10, 'bold'))
    patient_ID_entry = tk.Entry(AO_root, textvariable=patient_id_var, font=('calibre',10,'normal'))
    physician_name_label = tk.Label(AO_root, text = "Physician Name: ", font=('calibre',10, 'bold'))
    physician_name_entry = tk.Entry(AO_root, textvariable=physician_name_var, font=('calibre',10,'normal'))
    presc_med_label = tk.Label(AO_root, text = "Prescribed Medication: ", font=('calibre',10, 'bold'))
    presc_med_entry = tk.Entry(AO_root, textvariable=prescribed_med_var, font=('calibre',10,'normal'))
    med_ID_label = tk.Label(AO_root, text = "Medication ID: ", font=('calibre',10, 'bold'))
    med_ID_entry = tk.Entry(AO_root, textvariable=medication_id_var, font=('calibre',10,'normal'))
    dosage_label = tk.Label(AO_root, text = "Dosage: ", font=('calibre',10, 'bold'))
    dosage_entry = tk.Entry(AO_root, textvariable=dosage_var, font=('calibre',10,'normal'))
    freq_label = tk.Label(AO_root, text = "Medication Frequency: ", font=('calibre',10, 'bold'))
    freq_entry = tk.Entry(AO_root, textvariable=frequency_med_var, font=('calibre',10,'normal'))
    date_ordered_label = tk.Label(AO_root, text = "Date Ordered (MM/DD/YYYY): ", font=('calibre',10, 'bold'))
    date_ordered_entry = tk.Entry(AO_root, textvariable=date_ordered_var, font=('calibre',10,'normal'))
    date_filled_label = tk.Label(AO_root, text = "Date Filled (MM/DD/YYYY): ", font=('calibre',10, 'bold'))
    date_filled_entry = tk.Entry(AO_root, textvariable=date_filled_var, font=('calibre',10,'normal'))
    pharmacist_label =tk.Label(AO_root, text = "Pharmacist: ", font=('calibre',10, 'bold'))
    pharmacist_entry = tk.Entry(AO_root, textvariable=pharmacist_var, font=('calibre',10,'normal'))

    submit_button = tk.Button(AO_root, text="Submit", command = add_new_order)

    # TODO: need to check if prescription is already filled. 
    # TODO: need to create pop-ups/messages for errors.

    presc_ID_label.grid(row = 1, column = 0, pady = 5)
    presc_ID_entry.grid(row = 1, column = 1, pady = 5, sticky=W)
    patient_name_label.grid(row = 2, column = 0)
    patient_name_entry.grid(row = 2, column = 1, sticky=W)
    patient_ID_label.grid(row = 3, column = 0)
    patient_ID_entry.grid(row = 3, column = 1, sticky=W)
    physician_name_label.grid(row = 4, column = 0)
    physician_name_entry.grid(row = 4, column = 1, sticky=W)
    presc_med_label.grid(row=5, column=0)
    presc_med_entry.grid(row=5, column=1, sticky=W)
    med_ID_label.grid(row=6, column=0)
    med_ID_entry.grid(row=6, column=1, sticky=W)
    dosage_label.grid(row=7, column=0)
    dosage_entry.grid(row=7, column=1, sticky=W)
    freq_label.grid(row=8, column=0)
    freq_entry.grid(row=8, column=1, sticky=W)
    date_ordered_label.grid(row=9, column=0)
    date_ordered_entry.grid(row=9, column=1, sticky=W)
    date_filled_label.grid(row=10, column=0)
    date_filled_entry.grid(row=10, column=1, sticky=W)
    pharmacist_label.grid(row=11, column=0)
    pharmacist_entry.grid(row=11, column=1, sticky=W)

    submit_button.grid(row = 12, column = 0)

    AO_root.mainloop()


# TODO: still some todos that need to be completed in here
def CO_run_GUI(passed_user_id, passed_order_list, POT_var, root_window):
    CO_root = tk.Tk()
    CO_root.title("Complete Order")

    CO_root.geometry("400x350")

    def exit_entry():
        CO_root.destroy()
        root_window.destroy()
        initialize(passed_user_id)
    
    exit_button = tk.Button(CO_root, text='Back', command = exit_entry)
    exit_button.grid(row = 0, column = 0, pady = 5)

    pharmacist_var = tk.StringVar()
    date_filled_var = tk.StringVar()

    def complete():
        POT_var.PO_complete_order(passed_user_id, passed_order_list[PRESC_ID_LOC], pharmacist_entry.get(), date_filled_entry.get())
        CO_root.destroy()
        root_window.destroy()
        initialize(passed_user_id)


    presc_ID_label = tk.Label(CO_root, text = "Prescription ID: ", font=('calibre',10, 'bold'))
    presc_ID_label_2 = tk.Label(CO_root, text = passed_order_list[PRESC_ID_LOC], font=('calibre',10))
    patient_name_label = tk.Label(CO_root, text = "Patient Name: ", font=('calibre',10, 'bold'))
    patient_name_label_2 = tk.Label(CO_root, text = passed_order_list[PAT_NAME_LOC], font=('calibre',10))
    patient_ID_label = tk.Label(CO_root, text = "Patient ID: ", font=('calibre',10, 'bold'))
    patient_ID_label_2 = tk.Label(CO_root, text = passed_order_list[PAT_ID_LOC], font=('calibre',10))
    physician_name_label = tk.Label(CO_root, text = "Physician Name: ", font=('calibre',10, 'bold'))
    physician_name_label_2 = tk.Label(CO_root, text = passed_order_list[PHYS_NAME_LOC], font=('calibre',10))
    presc_med_label = tk.Label(CO_root, text = "Prescribed Medication: ", font=('calibre',10, 'bold'))
    presc_med_label_2 = tk.Label(CO_root, text = passed_order_list[PRESC_MED_LOC], font=('calibre',10))
    med_ID_label = tk.Label(CO_root, text = "Medication ID: ", font=('calibre',10, 'bold'))
    med_ID_label_2 = tk.Label(CO_root, text = passed_order_list[MED_ID_LOC], font=('calibre',10))
    dosage_label = tk.Label(CO_root, text = "Dosage: ", font=('calibre',10, 'bold'))
    dosage_label_2 = tk.Label(CO_root, text = passed_order_list[DOSAGE_LOC], font=('calibre',10))
    freq_label = tk.Label(CO_root, text = "Frequency: ", font=('calibre',10, 'bold'))
    freq_label_2 = tk.Label(CO_root, text = passed_order_list[FREQ_LOC], font=('calibre',10))
    date_ordered_label = tk.Label(CO_root, text = "Date Ordered: ", font=('calibre',10, 'bold'))
    date_ordered_label_2 = tk.Label(CO_root, text = passed_order_list[D_ORD_LOC], font=('calibre',10))
    date_filled_label = tk.Label(CO_root, text = "Date Filled (MM/DD/YYYY): ", font=('calibre',10, 'bold'))
    pharmacist_label =tk.Label(CO_root, text = "Pharmacist: ", font=('calibre',10, 'bold'))

    pharmacist_entry = tk.Entry(CO_root, textvariable=pharmacist_var, font=('calibre',10,'normal'))
    date_filled_entry = tk.Entry(CO_root, textvariable=date_filled_var, font=('calibre',10,'normal'))

    submit_button = tk.Button(CO_root, text="Complete", command = complete)

    # TODO: need to check if prescription is already filled. 
    # TODO: need to create pop-ups/messages for errors.

    presc_ID_label.grid(row = 1, column = 0, pady = 5)
    presc_ID_label_2.grid(row = 1, column = 1, pady = 5, sticky=W)
    patient_name_label.grid(row = 2, column = 0)
    patient_name_label_2.grid(row = 2, column = 1, sticky=W)
    patient_ID_label.grid(row = 3, column = 0)
    patient_ID_label_2.grid(row = 3, column = 1, sticky=W)
    physician_name_label.grid(row = 4, column = 0)
    physician_name_label_2.grid(row = 4, column = 1, sticky=W)
    presc_med_label.grid(row=5, column=0)
    presc_med_label_2.grid(row=5, column=1, sticky=W)
    med_ID_label.grid(row=6, column=0)
    med_ID_label_2.grid(row=6, column=1, sticky=W)
    dosage_label.grid(row=7, column=0)
    dosage_label_2.grid(row=7, column=1, sticky=W)
    freq_label.grid(row=8, column=0)
    freq_label_2.grid(row=8, column=1, sticky=W)
    date_ordered_label.grid(row=9, column=0)
    date_ordered_label_2.grid(row=9, column=1, sticky=W)
    date_filled_label.grid(row=10, column=0)
    date_filled_entry.grid(row=10, column=1, sticky=W)
    pharmacist_label.grid(row=11, column=0)
    pharmacist_entry.grid(row=11, column=1, sticky=W)

    submit_button.grid(row = 12, column = 0)

    CO_root.mainloop()

initialize("30242420")
# initialize("50323230")

# POT_var = PharmacyOrderTracking()

# POT_var.PO_add_order("46", "chuck norris", "Dr. Banner", "Ninja boost", "2330", "350 mg", "once a day", "10/25/2022", "11/03/2022", "Dr. Hwang")
#POT_var.PO_delete_pharmacy_order(46)


# FOR list as keys: https://www.geeksforgeeks.org/how-to-use-a-list-as-a-key-of-a-dictionary-in-python-3/
# FOR how to have 2 keys per 1 value https://stackoverflow.com/questions/10123853/how-do-i-make-a-dictionary-with-multiple-keys-to-one-value

# The PT subsystem shall maintain the following information on all medications that can be prescribed:
# This would require all medications to be stored in a medications database. 