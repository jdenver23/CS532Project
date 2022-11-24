#!/usr/bin/env python
import os
import csv
import sys
sys.path.insert(1, ".")
from pathlib import Path
from enum import Enum
from InsuranceBilling import USER_FILE, USER_FIELD, USER_FIELD_DELIMITER

EMPLOYEE_RANGE_L = 30000000
EMPLOYEE_RANGE_H = 40000000

base_folder = os.path.dirname(__file__)

def get_icon(icon_file_name):
    return os.path.join(base_folder, f"icons/{icon_file_name}")

def tk_center(tk, gui_w=None, gui_h=None):
    if gui_w is None:
        gui_w = tk.winfo_width()
    if gui_h is None:
        gui_h = tk.winfo_height()
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()
    
    x = (screen_width/2) - (gui_w/2)
    y = (screen_height/2) - (gui_h/2)
    tk.geometry('%dx%d+%d+%d' % (gui_w, gui_h, x, y))

class UIMode(Enum):
    PATIENT = 0
    EMPLOYEE = 1


class Patient:
    """ Patient is used for easier data management. """
    def __init__(self, id, first_name, last_name, email, phone_number, address, insurance_carrier, dob, gender, primary_care_physician, medications, appointments):
        self.id = id
        self.fname = first_name
        self.lname = last_name
        self.name = first_name + " " + last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.insurance_carrier = insurance_carrier
        self.dob = dob
        self.gender = gender
        self.primary_care_physician = primary_care_physician
        self.medications = medications
        self.appointments = appointments

class PatientAccount:
    """ PatientAcount is used to retrieve all users' information in the database. 
      \nIts main purpose is to provide a short description list of all users. """
    def __init__(self) -> None:
        if not Path(USER_FILE).is_file():
            open(USER_FILE, "a").close()
        
        self.patients: list[Patient] = []
        
        with open(USER_FILE, 'r') as f:
            for user in csv.DictReader(f, fieldnames=USER_FIELD, delimiter=USER_FIELD_DELIMITER):
                if not user[USER_FIELD[0]].isnumeric():
                    continue
                if int(user[USER_FIELD[0]]) >= EMPLOYEE_RANGE_H:
                    n_patient = Patient(id=user[USER_FIELD[0]], first_name=user[USER_FIELD[1]], last_name=user[USER_FIELD[2]], 
                                        email=user[USER_FIELD[3]], phone_number=user[USER_FIELD[5]], address=user[USER_FIELD[6]],
                                        insurance_carrier=user[USER_FIELD[7]], dob=user[USER_FIELD[8]], gender=user[USER_FIELD[9]], 
                                        primary_care_physician=user[USER_FIELD[10]], medications=user[USER_FIELD[11]], appointments=user[USER_FIELD[11]])
                    self.patients.append(n_patient)
    
    def as_description_list(self, opt="ID"):
        _list = []
        for patient in self.patients:
            if opt == "Name":
                tmp = ", ".join([patient.name, patient.id, patient.email, patient.dob, patient.phone_number])
            elif opt == "Email":
                tmp = ", ".join([patient.email, patient.name, patient.id, patient.dob, patient.phone_number])
            elif opt == "DOB":
                tmp = ", ".join([patient.dob, patient.email, patient.name, patient.id, patient.phone_number])
            elif opt == "Phone#":
                tmp = ", ".join([patient.phone_number, patient.dob, patient.email, patient.name, patient.id])
            else:
                tmp = ", ".join([patient.id, patient.name, patient.email, patient.dob, patient.phone_number])
            _list.append(tmp)
        return _list
            
    def get_patient(self, patient_id: str or int):
        patient_id = str(patient_id)
        for patient in self.patients:
            if patient.id == patient_id:
                return patient
        return None
    