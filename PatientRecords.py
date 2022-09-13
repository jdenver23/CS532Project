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