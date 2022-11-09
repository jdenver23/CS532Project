#-----------------------------------------------------
# CS 532 Software Engineering
# Class Project - Healthcare 
# 
# Author: Jonathan Lee
# PharmacyOrder.py
#
# Class to store the necessary information, getters, 
# and setters related to a single Pharmacy Order. 
# 
# Resources: https://www.youtube.com/watch?v=6uaVwyHFOk8
#            https://docs.python.org/2/library/csv.html
#            https://courses.cs.washington.edu/courses/cse140/13wi/csv-parsing.html 
#            https://learnpython.com/blog/read-csv-into-list-python/
#            https://www.geeksforgeeks.org/reading-rows-from-a-csv-file-in-python/
#            https://www.programiz.com/python-programming/datetime/strptime
#            https://www.geeksforgeeks.org/how-to-delete-only-one-row-in-csv-with-python/
#            https://thispointer.com/edit-cell-values-in-csv-files-using-pandas-in-python/
#            https://www.machinelearningplus.com/pandas/pandas-reset-index/
#-----------------------------------------------------
from calendar import calendar
import csv
from shutil import ReadError
from datetime import datetime
from datetime import date
import pandas as pd


class PharmacyOrder:
    csv_filename = "PharmacyOrder.csv"

    field_names = ['Prescription ID', 'Patient Name', 'Physician Name', 'Prescribed Medication', 'Medication ID', 'Dosage', 'Frequency', 'Date Ordered', 'Date Filled', 'Pharmacist']

    # Function to create a Pharmacy Order file (if it doesn't exist and give)
    #def __init__(self, prescription_id, patient_name, physician_name, medication, dosage, medication_frequency, date_filled, pharmacist):
    def __init__(self):
        # self.prescription_id = prescription_id
        # self.prescription_id = prescription_id
        # self.patient_name = patient_name
        # self.physician_name = physician_name
        # self.medication = medication
        # self.dosage = dosage
        # self.medication_frequency = medication_frequency
        # self.date_filled = date_filled
        # self.pharmacist = pharmacist
        pass

    #======================================================================================
    # # Getter methods for our class attributes
    # def get_prescription_id(self):
    #     return self.prescription_id
    
    # def get_patient_name(self):
    #     return self.patient_name
    
    # def get_physician_name(self):
    #     return self.physician_name
    
    # def get_medication(self):
    #     return self.medication
    
    # def get_dosage(self):
    #     return self.dosage
    
    # def get_medication_frequency(self):
    #     return self.medication_frequency
    
    # def get_date_filled(self):
    #     return self.date_filled
    
    # def get_pharmacist(self):
    #     return self.pharmacist
    
    # # Setter methods for our class attributes
    # def set_prescription_id(self, updated_presciption_id):
    #     self.prescription_id = updated_presciption_id
    
    # def set_patient_name(self, updated_patient_name):
    #     self.patient_name = updated_patient_name
    
    # def set_physician_name(self, updated_physician_name):
    #     self.physician_name = updated_physician_name
    
    # def set_medication(self, updated_medication):
    #     self.medication = updated_medication

    # def set_dosage(self, updated_dosage):
    #     self.dosage = updated_dosage
    
    # def set_medication_frequency(self, updated_medication_frequency):
    #     self.medication_frequency = updated_medication_frequency
    
    # def set_date_filled(self, updated_date_filled):
    #     self.date_filled = updated_date_filled
    
    # def set_pharmacist(self, updated_pharmacist):
    #     self.pharmacist = updated_pharmacist
    #======================================================================================

    
    # Add New functions
    # TODO: delete
    # def add_new_prescription_id(id):
    #     with open("PharmacyOrder.csv", mode = "a", newline = "") as f:
    #         writer = csv.writer(f, delimeter = ",")

    # TODO: need to check prescription ID when creating one to make sure it doesn't already exist. 
    # TODO: verification for each value is done likely somewhere else
    # TODO: will need to check user permissions later. 

    # Function to print a list of prescriptions
    def print_prescriptions(self, p_list):
        for presc in p_list:
            if len(p_list) == 0:
                print("ERROR: Unable to print the provided list!")
            print(presc)

    # Function to list all prescriptions ORDERED by a specific physician for a specific period of time 
    def prescriptions_ordered_by_physician(self, physician_name, start_time, end_time):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            # list to store all information of a match. 
            matching_prescriptions = list()

            # TODO: Can Update this to make patient name NOT case-sensitive
            for row in reader:
                # match with physician name and date ordered is not blank. 
                if row["Physician Name"] == physician_name and row["Date Ordered"] != "":
                    # check that date is in range
                    date_object = datetime.strptime(row["Date Ordered"], "%m/%d/%Y").date()
                    if date_object >= start_time and date_object <= end_time :
                        information_dictionary = PharmacyOrder.get_all_row_info(row)
                        matching_prescriptions.append(information_dictionary)
            
            # Return the list of matching prescriptions. if no match, then list is empty. 
            return matching_prescriptions

    # Function to list all prescriptions FILLED for a patient for a specific period of time
    # returns a list of matching prescriptions. otherwise, returns empty list. 
    def prescriptions_filled_for_patient(self, patient_name, start_time, end_time):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            matching_prescriptions = list()

            # TODO: Can Update this to make patient name NOT case-sensitive
            for row in reader:
                # if Date filled != "", then that means, prescription has been filled by a pharmacist.
                if row["Patient Name"] == patient_name and row["Date Filled"] != "":
                    # check that date is in range
                    date_object = datetime.strptime(row["Date Filled"], "%m/%d/%Y").date()
                    if date_object >= start_time and date_object <= end_time :
                        information_dictionary = PharmacyOrder.get_all_row_info(row)
                        matching_prescriptions.append(information_dictionary)
            
            # Return the list of matching prescriptions. if no match, then list is empty. 
            return matching_prescriptions

    # Function to provide a summary report by medication showing number of prescriptions filled by month and year filled and by physician. 
    def number_of_prescriptions_by_medication_month_physician(self):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            # dictionary to store number of prescriptions per medication per month and per physician.
            num_presc_dict = dict()
            
            # populate num_presc_dict
            for row in reader:
                # skip first row
                if row["Prescription ID"] == "Prescription ID":
                    continue
                # get medication, month, and physician
                medication = row["Prescribed Medication"]
                #TODO: should this by physician ID?
                physician = row["Physician Name"]
                if row["Date Filled"] == "":
                    # we don't add this prescription to our dictionary because it is not yet filled. 
                    continue
                date_object = datetime.strptime(row["Date Filled"], "%m/%d/%Y").date()
                month = date_object.month
                year = date_object.year
                
                key_tuple = (medication, month, year, physician)

                if key_tuple in num_presc_dict:
                    num_presc_dict[key_tuple] += 1
                else:
                    num_presc_dict[key_tuple] = 1

            return num_presc_dict

    # Function to map month number to month name. 
    # parameter month = month number as a string
    def month_name(self, month):
        names = {
            '01': 'January',
            '02': 'February',
            '03': 'March',
            '04': 'April',
            '05': 'May',
            '06': 'June',
            '07': 'July',
            '08': 'August',
            '09': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'December',
        }
        return names[month]

    # Function to give a report of the dictionary from number_of_prescriptions_by_medication_month_physician
    # keys of dict_result are tuples of size 4 as (medication, month, year, physician)
    def report_num_presc_by_medication_month_physician(self, dict_result):
        for key in dict_result:
            print("In " + self.month_name(str(key[1])) + " " + str(key[2]) + ", " + key[3] + " had " + str(dict_result[key]) + " prescriptions of " + key[0] + " filled.")

    # Function to add an order
    def add_order(self, prescription_id, patient_name, physician_name, medication, medication_id, dosage, medication_frequency, date_ordered, date_filled, pharmacist):
        # V1: Below is one way to add to a file, but it doesn't seem very wise in allowing for editing of fields
        # with open("PharmacyOrder.csv", mode = "a", newline = "") as f:
        #     writer = csv.writer(f, delimeter = ",")
        #     writer.writerow([prescription_id, patient_name, physician_name, medication, dosage, medication_frequency, date_filled, pharmacist])

        # TODO: need to make sure you don't add duplicate. 
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            for row in reader:
                if row["Prescription ID"] == prescription_id:
                    print("Prescription ID " + str(prescription_id) + " already exists and cannot be added.")
                    return

        with open(PharmacyOrder.csv_filename, mode = "a", newline = "") as f:
            writer = csv.DictWriter(f, fieldnames=PharmacyOrder.field_names)
            writer.writerow({
                "Prescription ID": prescription_id, 
                "Patient Name": patient_name.upper(),
                "Physician Name": physician_name, 
                "Prescribed Medication": medication.upper(),
                "Medication ID": medication_id,
                "Dosage": dosage,
                "Frequency": medication_frequency,
                "Date Ordered": date_ordered,
                "Date Filled": date_filled,
                "Pharmacist": pharmacist,
            })
            
        print("Successful Pharmacy Order added")

    # Function that gets all the information of a specific row and returns it as dictionary format.
    def get_all_row_info(row):
        info_dict = {\
            "Prescription ID": row["Prescription ID"],\
            "Patient Name": row["Patient Name"],\
            "Physician Name": row["Physician Name"],\
            "Prescribed Medication": row["Prescribed Medication"],\
            "Medication ID": row["Medication ID"],\
            "Dosage": row["Dosage"],\
            "Frequency": row["Frequency"],\
            "Date Ordered": row["Date Ordered"],\
            "Date Filled": row["Date Filled"],\
            "Pharmacist": row["Pharmacist"]}
        return info_dict


    # Function to print information(either the row information or an error message) of the result of search_by_prescription_id
    def print_search_by_prescription_id(self, dict_info, p_ID):
        if len(dict_info) == 0:
            print("No information found for prescription ID: " + p_ID)
        else:
            print(dict_info)

    # Function that searches based on prescription_id and returns a dictionary of the corresponding information
    # or otherwise an empty dictionary if there is no match. 
    # NOTE: if you search by prescription_id, you will only get one result.
    def search_by_prescription_id(self, prescription_id):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            for row in reader:
                if row["Prescription ID"] == prescription_id:
                    information_dictionary = PharmacyOrder.get_all_row_info(row)
                    return information_dictionary
            
            # if no match then return empty dictionary
            return dict()

    # Function to print information (either the a list of row information or an error message)
    def print_search_by_patient_name_and_medication(self, list_info, p_name, med):
        if len(list_info) == 0:
            print ("No information found for " + p_name + " with prescribed medication of " + med + ".")
        else:
            print(list_info)
 
    # Function that searches based on patient name and medication and returns a dictionary of the information
    # or otherwise an empty dictionary if there is no match. Returns a list of rows (which are of type dict())
    # NOTE: if you search by patient name and medication, it is possible to have more than 1 result.
    def search_by_patient_name_and_medication(self, patient_name, prescribed_medication):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            matches_list = list()

            # TODO: Can Update this to make patient name NOT case-sensitive
            for row in reader:
                if row["Patient Name"] == patient_name and row["Prescribed Medication"] == prescribed_medication:
                    information_dictionary = PharmacyOrder.get_all_row_info(row)
                    matches_list.append(information_dictionary)
            
            # If no match then return empty dictionary
            return matches_list

    # Function to delete pharmacy order by prescription ID. presc_ID is an integer value. 
    def delete_pharmacy_order(self, presc_ID):
        try:
            #  with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            pharm_order_df = pd.read_csv(PharmacyOrder.csv_filename)
            pharm_order_df = pharm_order_df.set_index("Prescription ID", inplace=False).drop(presc_ID, axis=0)
            print("Deleted Prescription with ID: " + str(presc_ID))

            pharm_order_df.to_csv(PharmacyOrder.csv_filename)
        except KeyError:
            print("Prescription with ID (" + str(presc_ID) + ") does not exist, so it cannot be deleted.")


    # Function to complete a prescription. Need to provide prescripion ID, pharmacist name, and date filled.
    # NOTE: p_ID must be an integer value.
    def complete_order(self, p_ID, pharmacist_name, date_filled):
        pharm_order_df = pd.read_csv(PharmacyOrder.csv_filename, index_col="Prescription ID")
        if pd.isna(pharm_order_df.loc[p_ID, "Pharmacist"]) and pd.isna(pharm_order_df.loc[p_ID, "Date Filled"]):
            pharm_order_df.loc[p_ID, "Pharmacist"] = pharmacist_name
            pharm_order_df.loc[p_ID, "Date Filled"] = date_filled
            # reset index so that prescription ID is added back to the dataFrame
            pharm_order_df = pharm_order_df.reset_index()
            pharm_order_df.to_csv(PharmacyOrder.csv_filename, index=False)
        else:
            print("Pharmacy Order " + str(p_ID) + " has already been completed.")
            return
                       
        
        print("Successfully Completed Presctiption Order " + str(p_ID))

#-----------Testing---------------
#first row of descriptions add TODO: maybe move this to init.

pharm_order = PharmacyOrder()
# pharm_order.add_order('Prescription ID', 'Patient Name', 'Physician Name', 'Prescribed Medication', 'Medication ID', 'Dosage', 'Frequency', 'Date Ordered', 'Date Filled', 'Pharmacist')

# Test 1 for add_order
# pharm_order.add_order("32", "jon lee", "dr. guzman", "Tylenol", "2442", "250 mg", "twice every 8 hours", "10/13/2022", "10/15/2022", "Dr. Hwang")
# pharm_order.add_order("22", "jar jar", "Dr. Banner", "Kryptonite", "2765", "400 mg", "once a day", "10/15/2022", "10/17/2022", "Dr. Casetti")
# pharm_order.add_order("34", "jon lee", "dr. guzman", "Sudafed", "2440", "250 mg", "once every 12 hours", "10/15/2022", "", "")
# pharm_order.add_order("35", "jon lee", "dr. guzman", "Vitamin C", "2566", "350 mg", "once a day", "10/01/2022", "10/03/2022", "Dr. Casetti")
# pharm_order.add_order("73", "mike winkder", "dr. guzman", "Vitamin C", "2566", "350mg", "once a day", "09/04/2022", "10/25/2022", "Dr. Casetti")
# pharm_order.add_order("46", "trevor dosner", "dr. guzman", "Vitamin C", "2566", "350mg", "once a day", "09/04/2022", "11/01/2022", "Dr. Casetti")
# pharm_order.add_order("39", "jon lee", "dr. guzman", "Vitamin C", "2566", "350 mg", "once a day", "10/22/2022", "11/01/2022", "Dr. Casetti")

pres_id = "32"
invalid_id = "33"   
name = "JON LEE"
invalid_name = 'JOH LEE'
presc_med = "TYLENOL"
invalid_med = "MOTRIN"
# Test 2 for search by prescription ID or patient name & medication
# info_dict = pharm_order.search_by_prescription_id(pres_id)
# info_list = pharm_order.search_by_patient_name_and_medication(name, "VITAMIN C")
#info_list = pharm_order.search_by_patient_name_and_medication("JAR JAR", "Kryptonite")
# if (len(info) == 0):
#     print("Prescription ID (" + invalid_id + ") does not exist.")
# else:
#     print(info)
# pharm_order.print_search_by_prescription_id(info_dict, pres_id)
# pharm_order.print_search_by_prescription_id(info_dict, invalid_id)
# pharm_order.print_search_by_patient_name_and_medication(info_list, name, presc_med)
# pharm_order.print_search_by_patient_name_and_medication(info_list, name, invalid_med)
# pharm_order.print_search_by_patient_name_and_medication(info_list, invalid_name, presc_med)
# pharm_order.print_search_by_patient_name_and_medication(info_list, name, "VITAMIN C")

# Test 3 for prescriptions_filled_by_patient()
# s_date = date(2022, 10, 1)
# e_date = date(2022, 10, 31)
# presc_filled_list = pharm_order.prescriptions_filled_for_patient("jon lee", s_date, e_date)
# pharm_order.print_prescriptions(presc_filled_list)

# Test 4 for prescriptions_filled_by_physician()
# s_date = date(2022, 10, 1)
# e_date = date(2022, 10, 15)
# presc_ordered_list = pharm_order.prescriptions_ordered_by_physician("Dr. Banner", s_date, e_date)
# pharm_order.print_prescriptions(presc_ordered_list)

# Test 5 for number_of_prescriptions_report_by_medication_month_physician
# filtered_dict = pharm_order.number_of_prescriptions_by_medication_month_physician()
# pharm_order.report_num_presc_by_medication_month_physician(filtered_dict)

# Test 6 for delete prescription by ID
# test_DNE_prescription_id = 44
# test_valid_prescription_id = 46
# pharm_order.delete_pharmacy_order(test_DNE_prescription_id)
# pharm_order.delete_pharmacy_order(test_valid_prescription_id)

# Test 7 Delete all for reset
# pharm_order.delete_pharmacy_order(32)
# pharm_order.delete_pharmacy_order(22)
# pharm_order.delete_pharmacy_order(34)
# pharm_order.delete_pharmacy_order(35)
# pharm_order.delete_pharmacy_order(73)
# pharm_order.delete_pharmacy_order(46)

# TEST 8 for complete pharmacy order
pharm_order.complete_order(34, "Dr. Casetti", "11/5/22")