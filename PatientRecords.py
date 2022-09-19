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