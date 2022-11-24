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
# 
#-----------------------------------------------------

import PharmacyOrder as PO
import Medications as MED
import CompleteOrder
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

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

class PharmacyOrderTracking:
    
    def __init__(self, user_ID):
        self.pharm_order_accessor = PO.PharmacyOrder()
        self.medication_accessor = MED.Medications()
        self.user_ID = user_ID
        pass
    
    def PO_add_order(self, user_ID, prescription_id, patient_name, physician_name, medication, medication_id, dosage, medication_frequency, date_ordered, date_filled, pharmacist):
        self.pharm_order_accessor.add_order(user_ID, prescription_id, patient_name, physician_name, medication, medication_id, dosage, medication_frequency, date_ordered, date_filled, pharmacist)
    
    def PO_delete_pharmacy_order(self, user_ID, presc_ID):
        self.pharm_order_accessor.delete_pharmacy_order(user_ID, presc_ID)
    
    def PO_print_prescriptions(self, p_list):
        self.pharm_order_accessor.print_prescriptions(p_list)
    
    def PO_prescriptions_ordered_by_physician(self, user_ID, physician_name, start_time, end_time):
        return self.pharm_order_accessor.prescriptions_ordered_by_physician(user_ID, physician_name, start_time, end_time)
    
    def PO_prescriptions_filled_for_patient(self, user_ID, patient_name, start_time, end_time):
        return self.pharm_order_accessor.prescriptions_filled_for_patient(user_ID, patient_name, start_time, end_time)
    
    def PO_number_of_prescriptions_by_medication_month_physician(self, user_ID):
        return self.pharm_order_accessor.number_of_prescriptions_by_medication_month_physician(user_ID)
    
    def PO_report_num_presc_by_medication_month_physician(self, dict_result):
        self.pharm_order_accessor.report_num_presc_by_medication_month_physician(dict_result)
    
    def PO_print_search_by_prescription_id(self, dict_info, p_ID):
        self.pharm_order_accessor.print_search_by_prescription_id(dict_info, p_ID)
    
    def PO_search_by_prescription_id(self, user_ID, prescription_id):
        return self.pharm_order_accessor.search_by_prescription_id(user_ID, prescription_id)

    def PO_print_search_by_patient_name_and_medication(self, list_info, p_name, med):
        self.pharm_order_accessor.print_search_by_patient_name_and_medication(list_info, p_name, med)
    
    def PO_search_by_patient_name_and_medication(self, user_ID, patient_name, prescribed_medication):
        return self.pharm_order_accessor.search_by_patient_name_and_medication(user_ID, patient_name, prescribed_medication)
    
    def PO_orders_to_be_filled(self, user_ID):
        return self.pharm_order_accessor.orders_to_be_filled(user_ID)
    
    def PO_orders_to_be_filled(self, user_ID):
        return self.pharm_order_accessor.orders_filled(user_ID)

    def PO_show_prescription_orders_list(self, user_ID):
        return self.pharm_order_accessor.show_prescription_orders_list(user_ID)
    
    def PO_complete_order(self, user_ID, presc_ID, pharmacist_name, date_filled):
        return self.pharm_order_accessor.complete_order(user_ID, presc_ID, pharmacist_name, date_filled)


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

    # listbox = Listbox(root, height = 500,
    #                 width = 500,
    #                 bg = "grey",
    #                 activestyle = 'dotbox',
    #                 font = "Helvetica",
    #                 fg = "black")

    root.geometry("1275x700")

    # style = ttk.Style()
    # style.theme_use('clam')

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
    home_button.grid(row=0, column=0, sticky='ns')

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
        # print(tree.selection()[0])
        # if len(tree.selection()) == 0:
        #     # TODO: needs to be changed later
        #     print("ERROR: Must select an order before clicking Complete Order.")
        #     return
        # if len(tree.selection()) == 1:
        #     # TODO: needs to be changed later
        #     print("ERROR: Only one order can be completed at a time.")
        #     return
        
        
        # CompleteOrder.open(POT_var.user_ID)
        root.destroy()
        # EditPatient.enter_prog(person.id_number)

    user_ID_int = int(POT_var.user_ID)
    if user_ID_int >= 30000000 and user_ID_int < 40000000:
        complete_order_button = ttk.Button(top, text='Complete Order', command = complete_order)
        # edit_button.pack(in_=top, side=LEFT)
        complete_order_button.grid(row=1, column=0, sticky='ns')

    root.mainloop()

# Iniital entry
def initialize(passed_user_id):
    # create Pharmacy Order Tracking (POT) instance with provided user ID. 
    POT_instance = PharmacyOrderTracking(passed_user_id)
    runGUI(POT_instance)


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