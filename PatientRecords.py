"""
<K,V> Name, ID Number
Create Account --> ID Number generated --> Added to <K,V>
Account --> Level, general info
Login info
This

To look up: db and python interfaces

Shall Include Patient:
ID Number
Name
Phone Number
Address
Insurance Carrier
Date of Birth
Gender
Primary Care physician
Current medications being taken
Current Appointments

Whoever made(read/write), specific patient(read),
practitioner seen(read/write)
MEDICAL ENCOUNTERS:
    Date
    Time
    Id of who made
    Id of patient
    Practitioner Seen
    Patient Complaints
    Vital Signs
    Practitioner Notes
    Lab Orders
    Diagnosis
    Treatment Plan
    Referral to Specialist
    Recommended Follow-up
"""
import csv
import tkinter as tk
import EditPatient
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class Patient:

    def __init__(self, id_number, patient_name, phone_number, address, insurance_carrier, date_of_birth, gender, primary_care_physician, current_meds, current_appointments):
        self.id_number = id_number
        self.patient_name = patient_name
        self.phone_number = phone_number
        self.address = address
        self.insurance_carrier = insurance_carrier
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.primary_care_physician = primary_care_physician
        self.current_meds = current_meds
        self.current_appointments = current_appointments

        def get_id_number(self):
            return self.id_number

        def set_id_number(self, x):
            self.id_number = x

        def get_patient_name(self):
            return self.patient_name

        def set_patient_name(self, x):
            self.patient_name = x
        
        def get_phone_number(self):
            return self.phone_number

        def set_phone_number(self, x):
            self.phone_number = x
        
        def get_address(self):
            return self.address

        def set_address(self, x):
            self.address = x
        
        def get_insurance_carrier(self):
            return self.insurance_carrier

        def set_insurance_carrier(self, x):
            self.insurance_carrier = x
        
        def get_date_of_birth(self):
            return self.date_of_birth

        def set_date_of_birth(self, x):
            self.date_of_birth = x

        def get_gender(self):
            return self.gender

        def set_gender(self, x):
            self.gender = x
        
        def get_primary_care_physician(self):
            return self.primary_care_physician

        def set_primary_care_physician(self, x):
            self.primary_care_physician = x
        
        def get_current_meds(self):
            return self.current_meds

        def set_current_meds(self, x):
            self.current_meds = x

        def get_current_appointments(self):
            return self.current_appointments

        def set_current_appointments(self, x):
            self.current_appointments = x

def runGui(person):
    root = tk.Tk()

    root.title("Patient Record")

    top = Frame(root)
    bottom = Frame(root)
    top.pack(side=TOP)
    bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

    listbox = Listbox(root, height = 500,
                    width = 500,
                    bg = "grey",
                    activestyle = 'dotbox',
                    font = "Helvetica",
                    fg = "black")

    root.geometry("500x500") 
    
    listbox.insert(1, "Patient Name: " + person.patient_name)
    listbox.insert(2, "")
    listbox.insert(3, "Phone Number: " + person.phone_number)
    listbox.insert(4, "")
    listbox.insert(5, "Address: " + person.address)
    listbox.insert(6, "")
    listbox.insert(7, "Insurance Carrier: " + person.insurance_carrier)
    listbox.insert(8, "")
    listbox.insert(9, "Date of Birth: " + person.date_of_birth)
    listbox.insert(10, "")
    listbox.insert(11, "Gender: " + person.gender)
    listbox.insert(12, "")
    listbox.insert(13, "Primary Care Physician: " + person.primary_care_physician)
    listbox.insert(14, "")
    listbox.insert(15, "Current Medications: " + person.current_meds)
    listbox.insert(16, "")
    listbox.insert(17, "Appointments: " + person.current_appointments)
    listbox.pack()

    home_button = ttk.Button(root, text='Home')
    home_button.pack(in_=top, side=LEFT)

    def edit_entry():
        root.destroy()
        EditPatient.enter_prog(person.id_number)

    edit_button = ttk.Button(root, text='Edit Information', command = edit_entry)
    edit_button.pack(in_=top, side=LEFT)

    def print_file():
        file_to_print = filedialog.askopenfilename(
        initialdir="/", title="Select file", 
        filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
      
        if file_to_print:
            os.ShellExecute(0, "print", file_to_print, None, ".", 0)

    save_button = ttk.Button(root, text="Save Page", command=print_file)
    save_button.pack(in_=top, side=RIGHT)
    
    root.mainloop()

def initialize(passed_id_number):
    with open("users.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0] == passed_id_number:
                instance = Patient(row[0], row[1] + " " + row[2], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
                runGui(instance)
