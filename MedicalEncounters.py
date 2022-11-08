class MedicalEncounters:

    def __init__(self, date, time,id_who_made, id_of_patient, practictioner_seen, patient_complaints, vital_signs, practitioner_notes,lab_orders,diagonosis, treatment_plan, referral_to_specialist,recommended_followup):
        self.date = date
        self.time = time 
        self.id_who_made = id_who_made
        self.id_patient = id_of_patient 
        self.practictioner_seen = practictioner_seen
        self.patient_complaints = patient_complaints
        self.vital_signs = vital_signs
        self.practitioner_notes = practitioner_notes 
        self.lab_orders = lab_orders
        self.diagnosis = diagonosis
        self.treatment_plan = treatment_plan
        self.referral_to_specialist= referral_to_specialist
        self.recommended_followup = recommended_followup


    # Acessor Methods for our Attributes
    def get_date(self):
        return self.date
    
    def get_time(self):
        return self.time
    
    def get_id_who_made(self):
        return self.id_who_made
   
    def get_id_patient(self):
        return self.id_patient
    
    def get_practictioner_seen(self):
        return self.practictioner_seen
    
    def get_patient_complaints(self):
        return self.patient_complaints
    
    def get_vital_signs(self):
        return self.vital_signs
    
    def get_practitioner_notes(self):
        return self.practitioner_notes
    
    def get_lab_orders(self):
        return self.lab_orders
    
    def get_diagnosis(self):
        return self.diagnosis
    
    def get_treatment_plan(self):
        return self.treatment_plan
    
    def get_referral_to_specialist(self):
        return self.referral_to_specialist

    def get_recommended_followup(self):
        return self.recommended_followup

    # Mutator Methods for our Attributes

    def set_date(self,new_date):
        self.date = new_date 
    
    def set_time(self,new_time):
        self.time = new_time
    
    def set_id_who_made(self,new_id_who_made):
        self.id_who_made = new_id_who_made
    
    def set_id_patient(self,new_id_patient):
        self.id_patient = new_id_patient 
    
    def set_practictioner_seen(self,new_practictioner_seen):
        self.practictioner_seen = new_practictioner_seen
    
    def set_patient_complaints(self,new_patient_complaints):
        self.patient_complaints = new_patient_complaints
    
    def set_vital_signs(self,new_vital_signs):
        self.vital_signs = new_vital_signs
    
    def set_practitioner_notes(self,new_practitioner_notes):
        self.practitioner_notes = new_practitioner_notes
    
    def set_lab_orders(self,new_lab_orders):
        self.lab_orders = new_lab_orders 
    
    def set_diagnosis(self,new_diagnosis):
        self.diagnosis = new_diagnosis
    
    def set_treatment_plan(self,new_treatment_plan):
        self.treatment_plan = new_treatment_plan
    
    def set_referral_to_specialist(self,new_referral_to_specialist):
        self.referral_to_specialist = new_referral_to_specialist
    
    def set_recommended_followup(self,new_recommended_followup):
        self.recommended_followup = new_recommended_followup

    
    




    

    