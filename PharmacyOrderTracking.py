#-----------------------------------------------------
# CS 532 Software Engineering
# Class Project - Healthcare 
# 
# Author: Jonathan Lee
# PharmacyOrderTracking.py
#
# Class to keep track of and execute necessary actions
# related to Pharmacy Orders. 
#-----------------------------------------------------

import PharmacyOrder as PO
import Medications as MED

class PharmacyOrderTracking:
    

    def __init__(self):
        self.pharm_order_accessor = PO.PharmacyOrder()
        self.medication_accessor = MED.Medications()
        pass
    
    def PO_add_order(self, prescription_id, patient_name, physician_name, medication, medication_id, dosage, medication_frequency, date_ordered, date_filled, pharmacist):
        self.pharm_order_accessor.add_order(prescription_id, patient_name, physician_name, medication, medication_id, dosage, medication_frequency, date_ordered, date_filled, pharmacist)
    
    def PO_delete_pharmacy_order(self, presc_ID):
        self.pharm_order_accessor.delete_pharmacy_order(presc_ID)
    
    def PO_print_prescriptions(self, p_list):
        self.pharm_order_accessor.print_prescriptions(p_list)
    
    def PO_prescriptions_ordered_by_physician(self, physician_name, start_time, end_time):
        return self.pharm_order_accessor.prescriptions_ordered_by_physician(physician_name, start_time, end_time)
    
    def PO_prescriptions_filled_for_patient(self, patient_name, start_time, end_time):
        return self.pharm_order_accessor.prescriptions_filled_for_patient(patient_name, start_time, end_time)
    
    def PO_number_of_prescriptions_by_medication_month_physician(self):
        return self.pharm_order_accessor.number_of_prescriptions_by_medication_month_physician()
    
    def PO_report_num_presc_by_medication_month_physician(self, dict_result):
        self.pharm_order_accessor.report_num_presc_by_medication_month_physician(dict_result)
    
    def PO_print_search_by_prescription_id(self, dict_info, p_ID):
        self.pharm_order_accessor.print_search_by_prescription_id(dict_info, p_ID)
    
    def PO_search_by_prescription_id(self, prescription_id):
        return self.pharm_order_accessor.search_by_prescription_id(prescription_id)

    def PO_print_search_by_patient_name_and_medication(self, list_info, p_name, med):
        self.pharm_order_accessor.print_search_by_patient_name_and_medication(list_info, p_name, med)
    
    def PO_search_by_patient_name_and_medication(self, patient_name, prescribed_medication):
        return self.pharm_order_accessor.search_by_patient_name_and_medication(patient_name, prescribed_medication)

POT_var = PharmacyOrderTracking()

# POT_var.PO_add_order("46", "chuck norris", "Dr. Banner", "Ninja boost", "2330", "350 mg", "once a day", "10/25/2022", "11/03/2022", "Dr. Hwang")
#POT_var.PO_delete_pharmacy_order(46)


# FOR list as keys: https://www.geeksforgeeks.org/how-to-use-a-list-as-a-key-of-a-dictionary-in-python-3/
# FOR how to have 2 keys per 1 value https://stackoverflow.com/questions/10123853/how-do-i-make-a-dictionary-with-multiple-keys-to-one-value

# The PT subsystem shall maintain the following information on all medications that can be prescribed:
# This would require all medications to be stored in a medications database. 