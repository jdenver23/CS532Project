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

    field_names = ['Prescription ID', 'Patient Name', 'Patient ID', 'Physician Name', 'Prescribed Medication', 'Medication ID', 'Dosage', 'Frequency', 'Date Ordered', 'Date Filled', 'Pharmacist']

    # Function to create a Pharmacy Order file (if it doesn't exist and give)
    #def __init__(self, prescription_id, patient_name, physician_name, medication, dosage, medication_frequency, date_filled, pharmacist):
    def __init__(self):
        pass


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
    # user_ID: string; physician_name: string; start_time_str: string; end_time_string
    # returns a list of dictionaries
    def prescriptions_ordered_by_physician_dict(self, user_ID, physician_name, start_time_str, end_time_str):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            # list to store all information of a match. 
            matching_prescriptions = list()

            # need to convert date_filled from string to Date object. 
            start_time = datetime.strptime(start_time_str, "%m/%d/%Y").date()
            end_time = datetime.strptime(end_time_str, "%m/%d/%Y").date()

            user_ID_int = int(user_ID)
            # if user is an employee, then display all presciptions that match query.
            if user_ID_int >= 30000000 and user_ID_int < 40000000:
                for row in reader:
                    # match with physician name and date ordered is not blank. 
                    if row["Physician Name"].upper() == physician_name.upper() and row["Date Ordered"] != "":
                        # check that date is in range
                        date_object = datetime.strptime(row["Date Ordered"], "%m/%d/%Y").date()
                        if date_object >= start_time and date_object <= end_time :
                            information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                            matching_prescriptions.append(information_dictionary)
            # if user is patient then only show that patient's prescriptions that match the query                
            else:
                for row in reader:
                    # match with physician name, user id, and date ordered is not blank. 
                    if row["Patient ID"] == user_ID and row["Physician Name"].upper() == physician_name.upper() and row["Date Ordered"] != "":
                        # check that date is in range
                        date_object = datetime.strptime(row["Date Ordered"], "%m/%d/%Y").date()
                        if date_object >= start_time and date_object <= end_time :
                            information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                            matching_prescriptions.append(information_dictionary)
            
            # Return the list of matching prescriptions. if no match, then list is empty. 
            return matching_prescriptions

    # Function to list all prescriptions ORDERED by a specific physician for a specific period of time 
    # user_ID: string; physician_name: string; start_time_str: string; end_time_string
    # returns a list of lists
    def prescriptions_ordered_by_physician_list(self, user_ID, physician_name, start_time_str, end_time_str):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            # list to store all information of a match. 
            matching_prescriptions = list()

            # need to convert date_filled from string to Date object. 
            start_time = datetime.strptime(start_time_str, "%m/%d/%Y").date()
            end_time = datetime.strptime(end_time_str, "%m/%d/%Y").date()

            user_ID_int = int(user_ID)
            # if user is an employee, then display all presciptions that match query.
            if user_ID_int >= 30000000 and user_ID_int < 40000000:
                for row in reader:
                    # match with physician name and date ordered is not blank. 
                    if row["Physician Name"].upper() == physician_name.upper() and row["Date Ordered"] != "":
                        # check that date is in range
                        date_object = datetime.strptime(row["Date Ordered"], "%m/%d/%Y").date()
                        if date_object >= start_time and date_object <= end_time :
                            information_dictionary = PharmacyOrder.get_all_row_info_list(row)
                            matching_prescriptions.append(information_dictionary)
            # if user is patient then only show that patient's prescriptions that match the query                
            else:
                for row in reader:
                    # match with physician name, user id, and date ordered is not blank. 
                    if row["Patient ID"] == user_ID and row["Physician Name"].upper() == physician_name.upper() and row["Date Ordered"] != "":
                        # check that date is in range
                        date_object = datetime.strptime(row["Date Ordered"], "%m/%d/%Y").date()
                        if date_object >= start_time and date_object <= end_time :
                            information_dictionary = PharmacyOrder.get_all_row_info_list(row)
                            matching_prescriptions.append(information_dictionary)
            
            # Return the list of matching prescriptions. if no match, then list is empty. 
            return matching_prescriptions

    # Function to list all prescriptions FILLED for a patient for a specific period of time
    # start_time_str: string; end_time_str: string
    # returns a list of dictionaries of matching prescriptions. otherwise, returns empty list. 
    # NOTE: if user is already a patient, then there should be some way that there is only one option for patient_name. 
    def prescriptions_filled_for_patient_dict(self, user_ID, patient_name, start_time_str, end_time_str):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            matching_prescriptions = list()

            # need to convert date_filled from string to Date object. 
            start_time = datetime.strptime(start_time_str, "%m/%d/%Y").date()
            end_time = datetime.strptime(end_time_str, "%m/%d/%Y").date()


            user_ID_int = int(user_ID)
            # if user is an employee, then display all presciptions that match query.
            if user_ID_int >= 30000000 and user_ID_int < 40000000:
                for row in reader:
                    # if Date filled != "", then that means, prescription has been filled by a pharmacist.
                    if row["Patient Name"] == patient_name.upper() and row["Date Filled"] != "":
                        # check that date is in range
                        date_object = datetime.strptime(row["Date Filled"], "%m/%d/%Y").date()
                        if date_object >= start_time and date_object <= end_time :
                            information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                            matching_prescriptions.append(information_dictionary)
            # if user is patient, then display only that user's prescriptions that match the query.
            else:
                for row in reader:
                    if row["Patient ID"] == user_ID and row["Patient Name"] == patient_name.upper() and row["Date Filled"] != "":
                        # check that date is in range
                        date_object = datetime.strptime(row["Date Filled"], "%m/%d/%Y").date()
                        if date_object >= start_time and date_object <= end_time :
                            information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                            matching_prescriptions.append(information_dictionary)
            
            # Return the list of matching prescriptions. if no match, then list is empty. 
            return matching_prescriptions

    # Function to list all prescriptions FILLED for a patient for a specific period of time
    # start_time_str: string; end_time_str: string
    # returns a list of list of matching prescriptions. otherwise, returns empty list. 
    # NOTE: if user is already a patient, then there should be some way that there is only one option for patient_name. 
    def prescriptions_filled_for_patient_list(self, user_ID, patient_name, start_time_str, end_time_str):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            matching_prescriptions = list()

            # need to convert date_filled from string to Date object. 
            start_time = datetime.strptime(start_time_str, "%m/%d/%Y").date()
            end_time = datetime.strptime(end_time_str, "%m/%d/%Y").date()

            user_ID_int = int(user_ID)
            # if user is an employee, then display all presciptions that match query.
            if user_ID_int >= 30000000 and user_ID_int < 40000000:
                for row in reader:
                    # if Date filled != "", then that means, prescription has been filled by a pharmacist.
                    if row["Patient Name"] == patient_name.upper() and row["Date Filled"] != "":
                        # check that date is in range
                        date_object = datetime.strptime(row["Date Filled"], "%m/%d/%Y").date()
                        if date_object >= start_time and date_object <= end_time :
                            information_list = PharmacyOrder.get_all_row_info_list(row)
                            matching_prescriptions.append(information_list)
            # if user is patient, then display only that user's prescriptions that match the query.
            else:
                for row in reader:
                    if row["Patient ID"] == user_ID and row["Patient Name"] == patient_name.upper() and row["Date Filled"] != "":
                        # check that date is in range
                        date_object = datetime.strptime(row["Date Filled"], "%m/%d/%Y").date()
                        if date_object >= start_time and date_object <= end_time :
                            information_list = PharmacyOrder.get_all_row_info_list(row)
                            matching_prescriptions.append(information_list)
            
            # Return the list of matching prescriptions. if no match, then list is empty. 
            return matching_prescriptions


    # TODO: needs documenting and testing
    def report_num_presc_by_medication_month_physician_list(self, user_id):
        dict_result = PharmacyOrder.number_of_prescriptions_by_medication_month_physician(user_id)

        result_list = list()

        for key in dict_result:
            result_str = "In " + self.month_name(str(key[1])) + " " + str(key[2]) + ", " + key[3].upper() + " had " + str(dict_result[key]) + " prescriptions of " + key[0] + " filled."
            result_list.append(result_str)
        
        return result_list

    # Function to provide a summary report by medication showing number of prescriptions filled by month and year filled and by physician. 
    # this should only be allowed to be accessed by employee. 
    # this called via report_num_presc_by_medication_month_physician_list()
    # NOTE: this function does not have the self argument because it is only accessed via the aforementioned function.
    def number_of_prescriptions_by_medication_month_physician(user_ID):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            # dictionary to store number of prescriptions per medication per month and per physician.
            num_presc_dict = dict()

            # make sure userID is not a patient. 
            user_ID_int = int(user_ID)
            # TODO: need to test for this!!
            # if user is a patient then return empty dictionary. 
            if user_ID_int >= 40000000:
                return num_presc_dict
            
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
    def add_order(self, user_id, prescription_id, patient_name, patient_id, physician_name, medication, medication_id, dosage, medication_frequency, date_ordered, date_filled, pharmacist):
        # V1: Below is one way to add to a file, but it doesn't seem very wise in allowing for editing of fields
        # with open("PharmacyOrder.csv", mode = "a", newline = "") as f:
        #     writer = csv.writer(f, delimeter = ",")
        #     writer.writerow([prescription_id, patient_name, physician_name, medication, dosage, medication_frequency, date_filled, pharmacist])

        # NOTE: if user is a patient, this operation cannot be accomplished
        user_id_int = int(user_id)
        if user_id_int >= 40000000:
            print("Patients are not authorized to add a Pharmacy Order")
            return


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
                "Patient ID": patient_id,
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
    def get_all_row_info_dict(row):
        info_dict = {\
            "Prescription ID": row["Prescription ID"],\
            "Patient Name": row["Patient Name"],\
            "Patient ID": row["Patient ID"],\
            "Physician Name": row["Physician Name"],\
            "Prescribed Medication": row["Prescribed Medication"],\
            "Medication ID": row["Medication ID"],\
            "Dosage": row["Dosage"],\
            "Frequency": row["Frequency"],\
            "Date Ordered": row["Date Ordered"],\
            "Date Filled": row["Date Filled"],\
            "Pharmacist": row["Pharmacist"]}
        return info_dict

    # Function that gets all the information of a specific row and returns it as list format.
    def get_all_row_info_list(row):
        info_list = [\
            row["Prescription ID"],\
            row["Patient Name"],\
            row["Patient ID"],\
            row["Physician Name"],\
            row["Prescribed Medication"],\
            row["Medication ID"],\
            row["Dosage"],\
            row["Frequency"],\
            row["Date Ordered"],\
            row["Date Filled"],\
            row["Pharmacist"]]
        return info_list

    # Function to print information(either the row information or an error message) of the result of search_by_prescription_id
    def print_search_by_prescription_id(self, dict_info, p_ID):
        if len(dict_info) == 0:
            print("No information found for prescription ID: " + p_ID)
        else:
            print(dict_info)

    # Function that searches based on prescription_id and returns a dictionary of the corresponding information
    # or otherwise an empty dictionary if there is no match. 
    # If user is a patient, they can only access a prescription (via its id) IF patient ID matches userID.
    # if user is an employee, they can access any prescription. 
    # NOTE: if you search by prescription_id, you will only get one result.
    # returns a dictionary.
    def search_by_prescription_id_dict(self, user_ID, prescription_id):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            user_id_int = int(user_ID)
            # if employee, then no restrictions besides original query
            if user_id_int >= 30000000 and user_id_int < 40000000:
                for row in reader:
                    if row["Prescription ID"] == prescription_id:
                        information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                        return information_dictionary
            # if patient
            else:
                for row in reader:
                    if user_ID == row["Patient ID"] and row["Prescription ID"] == prescription_id:
                        information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                        return information_dictionary
                    # print error message if prescription id matches but patient does not. 
                    if row["Prescription ID"] == prescription_id and user_ID != row["Patient ID"]:
                        print("ERROR: Patients are not allowed to access another patient's prescription orders")
            
            # if no match then return empty dictionary
            return dict()

    # Function that searches based on prescription_id and returns a dictionary of the corresponding information
    # or otherwise an empty dictionary if there is no match. 
    # If user is a patient, they can only access a prescription (via its id) IF patient ID matches userID.
    # if user is an employee, they can access any prescription. 
    # NOTE: if you search by prescription_id, you will only get one result.
    # returns a list.
    def search_by_prescription_id_list(self, user_ID, prescription_id):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            user_id_int = int(user_ID)
            # if employee, then no restrictions besides original query
            if user_id_int >= 30000000 and user_id_int < 40000000:
                for row in reader:
                    if row["Prescription ID"] == prescription_id:
                        information_dictionary = PharmacyOrder.get_all_row_info_list(row)
                        return information_dictionary
            # if patient
            else:
                for row in reader:
                    if user_ID == row["Patient ID"] and row["Prescription ID"] == prescription_id:
                        information_dictionary = PharmacyOrder.get_all_row_info_list(row)
                        return information_dictionary
                    # print error message if prescription id matches but patient does not. 
                    if row["Prescription ID"] == prescription_id and user_ID != row["Patient ID"]:
                        print("ERROR: Patients are not allowed to access another patient's prescription orders")
            
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
    # if user is patient, they should only allowed to be searching by their own medication. 
    # NOTE: if you search by patient name and medication, it is possible to have more than 1 result.
    # user_id: string, patient_name: string, prescribed_medication: string
    # returns a list of dictionaries
    # TODO: need to update tests. 
    def search_by_patient_name_and_medication_dict(self, user_id, patient_name, prescribed_medication):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            matches_list = list()

            user_id_int = int(user_id)
            # if user is an employee, then the user has full access to search by patient name and medication
            if user_id_int >= 30000000 and user_id_int < 40000000:
                for row in reader:
                    if row["Patient Name"] == patient_name.upper() and row["Prescribed Medication"] == prescribed_medication.upper():
                        information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                        matches_list.append(information_dictionary)
            # if user is a patient, then make sure patient is only seraching their records.    
            else:
                for row in reader:
                    if row["Patient Name"] == patient_name and row["Prescribed Medication"] == prescribed_medication and row["Patient ID"] == user_id:
                        information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                        matches_list.append(information_dictionary)
                    
                    # if patient name and user ID don't match, return empty list and shoot error message. 
                    if row["Patient Name"] == patient_name and row["Patient ID"] != user_id:
                        print("ERROR: Patients cannot access other Patient's pharmacy orders")
                        return list()
            
            # If no match then return empty list
            return matches_list

    # Function that searches based on patient name and medication and returns a dictionary of the information
    # or otherwise an empty dictionary if there is no match. Returns a list of rows (which are of type dict())
    # if user is patient, they should only allowed to be searching by their own medication. 
    # NOTE: if you search by patient name and medication, it is possible to have more than 1 result.
    # user_id: string, patient_name: string, prescribed_medication: string
    # returns a list of lists
    # TODO: need to add tests. 
    def search_by_patient_name_and_medication_list(self, user_id, patient_name, prescribed_medication):
        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)

            matches_list = list()

            user_id_int = int(user_id)
            # if user is an employee, then the user has full access to search by patient name and medication
            if user_id_int >= 30000000 and user_id_int < 40000000:
                for row in reader:
                    if row["Patient Name"] == patient_name.upper() and row["Prescribed Medication"] == prescribed_medication.upper():
                        information_list = PharmacyOrder.get_all_row_info_list(row)
                        matches_list.append(information_list)
            # if user is a patient, then make sure patient is only seraching their records.    
            else:
                for row in reader:
                    if row["Patient Name"] == patient_name.upper() and row["Prescribed Medication"] == prescribed_medication.upper() and row["Patient ID"] == user_id:
                        information_list = PharmacyOrder.get_all_row_info_list(row)
                        matches_list.append(information_list)
                    
                    # if patient name and user ID don't match, return empty list and shoot error message. 
                    if row["Patient Name"] == patient_name.upper() and row["Patient ID"] != user_id:
                        print("ERROR: Patients cannot access other Patient's pharmacy orders")
                        return list()
            
            # If no match then return empty list
            return matches_list

    # Function to delete pharmacy order by prescription ID. presc_ID is an integer value.
    # if user is patient, they don't have delete capabilities
    # if user is employee, then they have delete capabilities.  
    def delete_pharmacy_order(self, user_ID, presc_ID):
        # if user is patient, return with error messages and don't delete
        user_id_int = int(user_ID)
        if user_id_int >= 40000000:
            print("ERROR: Patient does not have Delete Pharmacy Order Permissions")
            return
        try:
            #  with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            pharm_order_df = pd.read_csv(PharmacyOrder.csv_filename)
            pharm_order_df = pharm_order_df.set_index("Prescription ID", inplace=False).drop(presc_ID, axis=0)
            print("Deleted Prescription with ID: " + str(presc_ID))

            pharm_order_df.to_csv(PharmacyOrder.csv_filename)
        except KeyError:
            print("Prescription with ID (" + str(presc_ID) + ") does not exist, so it cannot be deleted.")

    # function to show what prescriptions have not yet been filled. returns a list of information.
    # user ID is a string.
    def orders_to_be_filled(self, user_ID):
        not_yet_filled_list = list()

        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)
            # if the user is an employee
            if int(user_ID) >= 30000000 and int(user_ID) < 40000000:
                # allow for the user to view all prescriptions for any patient that need to be filled. 
                for row in reader:
                    if row["Date Filled"] == '':
                        information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                        not_yet_filled_list.append(information_dictionary)
            # if user is not employee
            else:
                # allow user to only view their prescriptions that need to be filled.
                for row in reader:
                    if row["Patient ID"] == user_ID and row["Date Filled"] == '':
                        information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                        not_yet_filled_list.append(information_dictionary)

        return not_yet_filled_list
            
    # function to show what prescriptions have been filled. 
    def orders_filled(self, user_ID):
        filled_list = list()

        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)
            # if the user is an employee
            if int(user_ID) >= 30000000 and int(user_ID) < 40000000:
                # allow for the user to view all prescriptions for any patient that need to be filled. 
                for row in reader:
                    if row["Date Filled"] != "" and row["Date Filled"] != "Date Filled":
                        information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                        filled_list.append(information_dictionary)
            # if user is not employee
            else:
                # allow user to only view their prescriptions that need to be filled.
                for row in reader:
                    if row["Patient ID"] == user_ID and row["Date Filled"] != '':
                        information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                        filled_list.append(information_dictionary)
        
        return filled_list

    # Function to show all prescriptions that is allowed by userID
    # returns a list of dictionaries.
    # TODO: need to update test with new name. 
    def show_prescription_orders_dict(self, user_ID):
        orders_list_of_dict = list()

        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)
            # if the user is an employee
            if int(user_ID) >= 30000000 and int(user_ID) < 40000000:
                # allow for the user to view all prescriptions 
                for row in reader:
                    # skip the header row
                    if row["Prescription ID"] != "Prescription ID":
                        information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                        orders_list_of_dict.append(information_dictionary)
            # if user is not employee
            else:
                # allow user to only view their prescriptions that need to be filled.
                for row in reader:
                    if row["Patient ID"] == user_ID:
                        information_dictionary = PharmacyOrder.get_all_row_info_dict(row)
                        orders_list_of_dict.append(information_dictionary)
        
        return orders_list_of_dict
    

    # Function to show all prescriptions that is allowed by userID
    # returns a list of list.
    # TODO: needs to be tested
    def show_prescription_orders_list(self, user_ID):
        orders_list_of_list = list()

        with open(PharmacyOrder.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=PharmacyOrder.field_names)
            # if the user is an employee
            if int(user_ID) >= 30000000 and int(user_ID) < 40000000:
                # allow for the user to view all prescriptions 
                for row in reader:
                    # skip the header row
                    if row["Prescription ID"] != "Prescription ID":
                        information_dictionary = PharmacyOrder.get_all_row_info_list(row)
                        orders_list_of_list.append(information_dictionary)
            # if user is not employee
            else:
                # allow user to only view their prescriptions that need to be filled.
                for row in reader:
                    if row["Patient ID"] == user_ID:
                        information_dictionary = PharmacyOrder.get_all_row_info_list(row)
                        orders_list_of_list.append(information_dictionary)
        
        return orders_list_of_list

    # Function to complete a prescription. Need to provide prescripion ID, pharmacist name, and date filled.
    # date_filled must be a Date object.
    # only Employee users have permission to complete orders.
    # user_ID is a string, presc_ID is a string, pharmacist_name is a string, and date_filled is a string. 
    # NOTE: presc_ID must be an integer value.
    def complete_order(self, user_ID, presc_ID, pharmacist_name, date_filled_str):
        user_id_int = int(user_ID)
        presc_ID_int = int(presc_ID)

        # need to convert date_filled from string to Date object. 
        date_filled = datetime.strptime(date_filled_str, "%m/%d/%Y").date()

        if user_id_int >= 40000000: 
            print("ERROR: Patients do not have Complete Order capabilities.")
            return

        pharm_order_df = pd.read_csv(PharmacyOrder.csv_filename, index_col="Prescription ID")
        if pd.isna(pharm_order_df.loc[presc_ID_int, "Pharmacist"]) and pd.isna(pharm_order_df.loc[presc_ID_int, "Date Filled"]):
            pharm_order_df.loc[presc_ID_int, "Pharmacist"] = pharmacist_name
            # check to make sure that Date filled is after date ordered. 
            date_object_ordered = datetime.strptime(pharm_order_df.loc[presc_ID_int, "Date Ordered"], "%m/%d/%Y").date()
            # if date filled is before date ordered, then print error
            if date_filled < date_object_ordered:
                print("ERROR: Failed to Complete Prescription Order - Date Filled is before Date Ordered.")
                return
            else:
                # update date filled, but first convert it to string.                                                                                                                                                                   
                pharm_order_df.loc[presc_ID_int, "Date Filled"] = date_filled.strftime("%m/%d/%Y")
            # reset index so that prescription ID is added back to the dataFrame
            pharm_order_df = pharm_order_df.reset_index()
            pharm_order_df.to_csv(PharmacyOrder.csv_filename, index=False)
        else:
            print("Pharmacy Order " + str(presc_ID_int) + " has already been completed.")
            return
                       
        
        print("Successfully Completed Presctiption Order " + str(presc_ID))

#-----------Testing---------------
#first row of descriptions add TODO: maybe move this to init.

pharm_order = PharmacyOrder()
# pharm_order.add_order('Prescription ID', 'Patient Name', 'Patient ID', 'Physician Name', 'Prescribed Medication', 'Medication ID', 'Dosage', 'Frequency', 'Date Ordered', 'Date Filled', 'Pharmacist')

# Test 1 for add_order
# 1.1: valid inputs with valid user adding orders
# pharm_order.add_order("30323230", "32", "jon lee", "50323230", "dr. guzman", "Tylenol", "2442", "250 mg", "twice every 8 hours", "10/13/2022", "10/15/2022", "Dr. Hwang")
# pharm_order.add_order("30323230", "22", "jar jar", "60242420", "Dr. Banner", "Kryptonite", "2765", "400 mg", "once a day", "10/15/2022", "10/17/2022", "Dr. Casetti")
# pharm_order.add_order("30323230", "34", "jon lee", "50323230", "dr. guzman", "Sudafed", "2440", "250 mg", "once every 12 hours", "10/15/2022", "", "")
# pharm_order.add_order("30323230", "35", "jon lee", "50323230", "dr. guzman", "Vitamin C", "2566", "350 mg", "once a day", "10/01/2022", "10/03/2022", "Dr. Casetti")
# pharm_order.add_order("30323230", "73", "mike winkder", "52056756", "dr. guzman", "Vitamin C", "2566", "350mg", "once a day", "09/04/2022", "10/25/2022", "Dr. Casetti")
# pharm_order.add_order("30323230", "46", "trevor dosner", "85882422", "dr. guzman", "Vitamin C", "2566", "350mg", "once a day", "09/04/2022", "", "")
# pharm_order.add_order("30323230", "39", "jon lee", "50323230", "dr. guzman", "Vitamin C", "2566", "350 mg", "once a day", "10/22/2022", "", "")
# pharm_order.add_order("30323230", "40", "jar jar", "60242420", "dr. guzman", "Vitamin D", "2586", "350 mg", "once a day", "10/13/2022", "10/15/22", "Dr. Hwang")
# 1.2 Invalid user attempts adding orders
# pharm_order.add_order("50323230", "41", "Anakin", "60477420", "dr. guzman", "Vitamin B", "2586", "350 mg", "once a day", "10/13/2022", "10/15/22", "Dr. Hwang")

pres_id = "32"
invalid_id = "33"   
someone_else_presc_id = "22"
name = "JON LEE"
invalid_name = 'JOH LEE'
presc_med = "TYLENOL"
invalid_med = "Vitamin Z"
# Test 2 for search by prescription ID or patient name & medication
# 2.1 Patient User searches for their own prescription that exists.
# info_dict = pharm_order.search_by_prescription_id("50323230", pres_id)
# pharm_order.print_search_by_prescription_id(info_dict, pres_id)
# 2.2 Patient User searches for their own prescription that does not exist.
# info_dict = pharm_order.search_by_prescription_id("50323230", invalid_id)
# pharm_order.print_search_by_prescription_id(info_dict, invalid_id)
# 2.3 Patient User searches for someone else's prescription that does exist.  
# info_dict = pharm_order.search_by_prescription_id("50323230", someone_else_presc_id)
# pharm_order.print_search_by_prescription_id(info_dict, someone_else_presc_id)
# 2.4 Employee User searches for valid prescription id
# info_dict = pharm_order.search_by_prescription_id("30323230", someone_else_presc_id)
# pharm_order.print_search_by_prescription_id(info_dict, someone_else_presc_id)
# 2.5 Employee User searches for invalid prescription id
# info_dict = pharm_order.search_by_prescription_id("30323230", invalid_id)
# pharm_order.print_search_by_prescription_id(info_dict, invalid_id)

# 2.6 Employee user searches by patient name and medication. 
# info_list = pharm_order.search_by_patient_name_and_medication("30323230", name, "VITAMIN C")
# pharm_order.print_search_by_patient_name_and_medication(info_list, name, "VITAMIN C")
# 2.7 Employee searches by invalid patient name but valid medication
# info_list = pharm_order.search_by_patient_name_and_medication("30323230", invalid_name, "VITAMIN C")
# pharm_order.print_search_by_patient_name_and_medication(info_list, invalid_name, "VITAMIN C")
# 2.8 Employee searches by valid patient name but invalid medication
# info_list = pharm_order.search_by_patient_name_and_medication("30323230", name, invalid_med)
# pharm_order.print_search_by_patient_name_and_medication(info_list, name, invalid_med)
# 2.9 Patient searches by their own name and medication.
# info_list = pharm_order.search_by_patient_name_and_medication("50323230", name, "VITAMIN C")
# pharm_order.print_search_by_patient_name_and_medication(info_list, name, "VITAMIN C")
# 2.10 Patient user search by someone else's name and valid medication. 
# info_list = pharm_order.search_by_patient_name_and_medication("70323230", name, "VITAMIN C")
# pharm_order.print_search_by_patient_name_and_medication(info_list, name, "VITAMIN C")
# 2.11 Patient User search by their own name but invalid madication. 
# info_list = pharm_order.search_by_patient_name_and_medication("50323230", name, invalid_med)
# pharm_order.print_search_by_patient_name_and_medication(info_list, name, invalid_med)

# Test 3 for prescriptions_filled_by_patient()
# s_date = date(2022, 10, 1)
# e_date = date(2022, 10, 31)
# 3.1: Test for employeeID given patient name and date range. should show matching query.
# presc_filled_list = pharm_order.prescriptions_filled_for_patient("30245442", "JON LEE", s_date, e_date)
# pharm_order.print_prescriptions(presc_filled_list)
# 3.2 Test for patientID given patient name and date range. also patient id matches correct patient name. 
# presc_filled_list = pharm_order.prescriptions_filled_for_patient("50323230", "JON LEE", s_date, e_date)
# pharm_order.print_prescriptions(presc_filled_list)
# 3.3 Test for patient ID where it doesn't match patient name. user patient trying to access someone else's information.
# presc_filled_list = pharm_order.prescriptions_filled_for_patient("60242420", "JON LEE", s_date, e_date)
# pharm_order.print_prescriptions(presc_filled_list)
# 3.4 Test for employee ID with non-existent patient name. 
# presc_filled_list = pharm_order.prescriptions_filled_for_patient("30245442", "JOE LEE", s_date, e_date)
# pharm_order.print_prescriptions(presc_filled_list)

# Test 4 for prescriptions_filled_by_physician()
# s_date = date(2022, 10, 1)
# e_date = date(2022, 10, 15)
# 4.1: Test for prescription ordered by specified physician with specified date range given specified patient
# presc_ordered_list = pharm_order.prescriptions_ordered_by_physician("60242420", "Dr. Banner", s_date, e_date)
# pharm_order.print_prescriptions(presc_ordered_list)
# 4.2 Test for prescription ordered by specified physician with specified date range for an employee
# presc_ordered_list = pharm_order.prescriptions_ordered_by_physician("30323230", "dr. guzman", s_date, e_date)
# pharm_order.print_prescriptions(presc_ordered_list)
# 4.3 test for prescription ordered invalid patient ID
# presc_ordered_list = pharm_order.prescriptions_ordered_by_physician("50523230", "dr. guzman", s_date, e_date)
# pharm_order.print_prescriptions(presc_ordered_list)

# TODO: these tests need to be updated because the function is now only accessed from other functions. no longer has self parameter. 
# Test 5 for number_of_prescriptions_report_by_medication_month_physician
# 5.1 Test given verified employee who has access this data.
# filtered_dict = pharm_order.number_of_prescriptions_by_medication_month_physician("30323230")
# pharm_order.report_num_presc_by_medication_month_physician(filtered_dict)
# 5.2: Test given patient who should not have access to this information.
# filtered_dict = pharm_order.number_of_prescriptions_by_medication_month_physician("60242420")
# pharm_order.report_num_presc_by_medication_month_physician(filtered_dict)

# Test 6 for delete prescription by ID
# pharm_order.add_order("30323230", "42", "Grogu", "60478492", "dr. guzman", "Vitamin B", "2586", "350 mg", "once a day", "10/13/2022", "10/15/22", "Dr. Hwang")
# test_DNE_prescription_id = 41
# test_valid_prescription_id = 42
# 6.1 Test for Employee User for prescription that does not exist. 
# pharm_order.delete_pharmacy_order("30323230", test_DNE_prescription_id)
# 6.2 Test for Employee User for prescription that does exist
# pharm_order.delete_pharmacy_order("30323230", test_valid_prescription_id)
# 6.3 Test for Patient User for prescription that does not exist.
# pharm_order.delete_pharmacy_order("40000000", test_DNE_prescription_id)
# 6.4 Test for Patient User for prescription that does exist
# pharm_order.delete_pharmacy_order("40000000", test_valid_prescription_id)

# Test 7 Delete all for reset
# pharm_order.delete_pharmacy_order("30323230", 32)
# pharm_order.delete_pharmacy_order("30323230", 22)
# pharm_order.delete_pharmacy_order("30323230", 34)
# pharm_order.delete_pharmacy_order("30323230", 35)
# pharm_order.delete_pharmacy_order("30323230", 73)
# pharm_order.delete_pharmacy_order("30323230", 46)
# pharm_order.delete_pharmacy_order("30323230", 39)

# TEST 8 for complete pharmacy order
# pharm_order.add_order("30323230", "43", "Mando", "60413492", "dr. guzman", "Vitamin X", "2586", "350 mg", "once a day", "10/13/2022", "", "")
# 8.1 Patient User attempts to complete order with valid date. Should Fail
# pharm_order.complete_order("50323230", "43", "Dr. Casetti", "10/14/2022")
# 8.2 Patient User attempts to complete order with current date before date ordered. Should Fail
# pharm_order.complete_order("50323230", "43", "Dr. Casetti", "10/11/2022")
# 8.3 Employee user attempts to complete order when date filled is before date ordered. Should Fail
# pharm_order.complete_order("30323230", "43", "Dr. Casetti", "10/11/2022")
# 8.4 Employee user attempt sto complete order with valid date.
# pharm_order.complete_order("30323230", "43", "Dr. Casetti", "10/14/2022")
# pharm_order.delete_pharmacy_order("30323230", 43)

# Test 9 for displaying not yet filled orders. 
# 9.1 test for employee, make sure all unfilled prescriptions shown. 
# print(pharm_order.orders_to_be_filled("30245442"))
# 9.2 test for user, make sure shows only unfileed for specific user
# print(pharm_order.orders_to_be_filled("50323230"))
# 9.3 test for when userID does not exist. 
# print(pharm_order.orders_to_be_filled("40024244"))

# Test 10 for displaying filled for orders. given a specificed user
# 10.1 test for employee, make sure all filled prescriptions shown. 
# print(pharm_order.orders_filled("30245442"))
# 10.2 test for patient, make sure to only show prescriptions for specific user.
# print(pharm_order.orders_filled("50323230"))
# 10.3 test for when userID does not exist. 
# print(pharm_order.orders_filled("40024244"))

# Test 11 for displaying all orders depending on the userID
# 11.1 test for employee ID. show all prescriptions filled or not.
# print(pharm_order.show_prescription_orders_dict("30245442"))
# 11.2 test for patient ID. show all prescriptions filled or not for the give patient
# print(pharm_order.show_prescription_orders_dict("50323230"))
# 11.3 test for non-existent ID
# print(pharm_order.show_prescription_orders_dict("40024244"))