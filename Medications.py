#-----------------------------------------------------
# CS 532 Software Engineering
# Class Project - Healthcare 
# 
# Author: Jonathan Lee
# Medications.py
#
# Class to store the necessary information, getters, 
# and setters related to a single Medication. 
#-----------------------------------------------------
import csv


class Medications: 
    csv_filename = "Medications.csv"
    # TODO: maybe consider name change for potential side effects and caution drugs (name also) because they are both lists.
    field_names = ['Medication ID', 'Medication Name', 'Description', 'Recommended Dosage', 'Recommended Frequency', 'Potential Side Effects', 'Caution Drugs']

    #def __init__(self, medication_id, medication_name, medication_description, recommended_dosage, recommended_frequency, list_side_effects, list_caution_drugs):
    def __init__(self):
        # self.medication_id = medication_id
        # self.medication_name = medication_name
        # self.medication_description = medication_description
        # self.recommended_dosage = recommended_dosage
        # self.recommended_frequency = recommended_frequency
        # self.list_side_effects = list_side_effects
        # self.list_caution_drugs = list_caution_drugs
        pass

    # Getters for class attributes
    # def get_medication_id(self):
    #     return self.medication_id
    
    # def get_medication_name(self):
    #     return self.medication_name
    
    # def get_medication_description(self):
    #     return self.medication_description
    
    # def get_recommended_dosage(self):
    #     return self.recommended_dosage

    # def get_recommended_frequency(self):
    #     return self.recommended_frequency
    
    # def get_list_side_effects(self):
    #     return self.list_side_effects
    
    # def get_list_caution_drugs(self):
    #     return self.list_side_effects
    
    # # Setters for class attributes
    # def set_medication_id(self, new_medication_id):
    #     self.medication_id = new_medication_id
    
    # def set_medication_name(self, new_medication_name):
    #     self.medication_name = new_medication_name
    
    # def set_medication_description(self, new_medication_description):
    #     self.medication_description = new_medication_description
    
    # def set_recommended_dosage(self, new_recommended_dosage):
    #     self.recommended_dosage = new_recommended_dosage
    
    # def set_recommended_frequency(self, new_recommended_frequency):
    #     self.recommended_frequency = new_recommended_frequency

    # def set_list_side_effects(self, new_list_side_effects):
    #     self.list_side_effects = new_list_side_effects
    
    # def set_list_caution_drugs(self, new_list_caution_drugs):
    #     self.list_caution_drugs = new_list_caution_drugs

    #===============================================================================
    

    
    # Since side effects and caution drugs are lists, they will probably need adders to 
    # append to the end of the list. 

    # function providing a summary report by medication showing number of prescriptions
    # filled by month and by physician. 
    # i.e. for medication X: 
    #          A prescriptions in January ordered by Dr. Jones
    #          B prescriptions in March ordered by Dr. Jones
    #          B prescriptions in January ordered by Dr. Walker
    #      for medication Y: 

    # function to add medication
    def add_medication(self, medication_id, medication_name, medication_description, recommended_dosage, recommended_frequency, list_side_effects, list_caution_drugs):

        # TODO: need to check if adding one that already exists
        with open(Medications.csv_filename, mode = "a", newline = "") as f:
            writer = csv.DictWriter(f, fieldnames=Medications.field_names)
            writer.writerow({
                "Medication ID": medication_id,
                "Medication Name": medication_name,
                "Description": medication_description,
                "Recommended Dosage": recommended_dosage,
                "Recommended Frequency": recommended_frequency, 
                "Potential Side Effects": list_side_effects,
                "Caution Drugs": list_caution_drugs,
            })
        
        print("Successful Medication Added")

    # Function that gets all the information of a specific row and returns it as dictionary format.
    def get_all_row_info(row):
        info_dict = {\
            "Medication ID": row["Medication ID"],\
            "Medication Name": row["Medication Name"],\
            "Description": row["Description"],\
            "Recommended Dosage": row["Recommended Dosage"],\
            "Recommended Frequency": row["Recommended Frequency"],\
            "Potential Side Effects": row["Potential Side Effects"],\
            "Caution Drugs": row["Caution Drugs"]}
        return info_dict

    # Function that searches based on medication ID and returns a dictionary of the corresponding information
    # or otherwise an empty dictionary if there is no match. 
    def search_by_medication_id(self, medication_id):
        with open(Medications.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=Medications.field_names)

            for row in reader:
                if row["Medication ID"] == medication_id:
                    information_dictionary = Medications.get_all_row_info(row)
                    return information_dictionary
            
            # if no match then return empty dictionary
            return dict()
    
    # Function that searches based on medication name and returns a dictionary of the corresponding information
    # or otherwise an empty dictionary if there is no match. 
    def search_by_medication_name(self, medication_name):
        with open(Medications.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=Medications.field_names)

            for row in reader:
                if row["Medication Name"] == medication_name:
                    information_dictionary = Medications.get_all_row_info(row)
                    return information_dictionary
            
            # if no match then return empty dictionary
            return dict()


#---------------Testing---------------

def test_search_by_medication_name(name):
    info_by_name = med.search_by_medication_name(name)
    if (len(info_by_name) == 0):
        print("Prescription Name (" + name + ") does not exist.")
    else:
        print(info_by_name)

def test_search_by_medication_id(id):
    info_by_id = med.search_by_medication_id(id)
    if (len(info_by_id) == 0):
        print("Prescription ID (" + id + ") does not exist.")
    else:
        print(info_by_id)

med = Medications()
# med.add_medication("2442", "Tylenol", "Pain reliever and fever reducer", "500 mg", "2 tablets every 4 hours", " hives; difficulty breathing; swelling of your face, lips, tongue, or throat", "carbamazepine, isoniazid, rifampin, alcohol, cholestyramine, and warfarin")
# med.add_medication("2440", "Sudafed", "Decongestant", "240 mg", "1 Tablet every 12 hours", "weakness or dizziness; restlessness; headache", "MAO inhibitors; caffeine")

med_name_right = "Sudafed"
med_name_wrong = "Motrin"

# test_search_by_medication_name(med_name_right)
# test_search_by_medication_name(med_name_wrong)

med_id_right = "2442"
med_id_wrong = "2441"

# test_search_by_medication_id(med_id_right)
# test_search_by_medication_id(med_id_wrong)