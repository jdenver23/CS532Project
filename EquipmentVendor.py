from enum import Enum
from pathlib import Path
import os
import csv
import pandas as pd
from datetime import datetime



class EquipmentVendor: 
    
    csv_filename = "EquipmentVendor.csv"
    field_names = ['Vendor ID', 'Vendor name', 'Vendor address', 'Equipment Type', 'Preference']

    def info(row):
        info_dict = {\
            "Vendor ID": row["Vendor ID"],\
            "Vendor name": row["Vendor name"],\
            "Vendor address" : row["Vendor address"],\
            "Equipment Type": row["Equipment Type"],\
            "Preference": row["Preference"]
       }
        return info_dict
        print(info_dict)
        
    def display_all(self):
        
        with open('EquipmentVendor.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
                
    
    def remove_vendor(self, vendor_id):
        lines = list()
        vendor = input("Please enter a vendor Id to be deleted.")
        with open('EquipmentVendor.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == vendor:
                        lines.remove(row)

        with open('EquipmentVendor.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
            
        print ("Vendor Removed")  
        
         

    def add_vendor(self, vendor_id, vendor_name, vendor_address, equipment_type, preference):

        with open(EquipmentVendor.csv_filename, mode = "a", newline = "") as f:
            writer = csv.DictWriter(f, fieldnames=EquipmentVendor.field_names)
            writer.writerow({
                "Vendor ID": vendor_id,
                "Vendor name": vendor_name,
                "Vendor address" : vendor_address,
                "Equipment Type": equipment_type,
                "Preference" : preference,
             
            })
        
        print("Vendor Added")

  
    # Function for the EQ subsystem shall allow the user to query the equipment vendor information by vendor ID, vendor name, and equipment type.
    
    def search_by_vendor_id(self, vendor_id):
        with open(EquipmentVendor.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=EquipmentVendor.field_names)

            for row in reader:
                if row["Vendor ID"] == vendor_id:
                    information_dictionary = EquipmentVendor.info(row)
                    return information_dictionary
            
            return dict()
    
    def search_by_vendor_name(self, vendor_name):
        with open(EquipmentVendor.csv_filename,mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=EquipmentVendor.field_names)

            for row in reader:
                if row["Vendor name"] == vendor_name:
                    information_dictionary = EquipmentVendor.info(row)
                    return information_dictionary
            
            return dict()
        
    def search_by_equipment_type(self, equipment_type):
        with open(EquipmentVendor.csv_filename, newline = "") as f:
            reader = csv.DictReader(f, fieldnames=EquipmentVendor.field_names)

            for row in reader:
                if row["Equipment Type"] == equipment_type:
                    information_dictionary = EquipmentVendor.info(row)
                    return information_dictionary
                        
            return dict()





#---------------Testing---------------



def test_search_by_vendor_name(name):
    info_by_name = ven.search_by_vendor_name(name)
    if (len(info_by_name) == 0):
        print("vendor Name (" + name + ") does not exist.")
    else:
        print(info_by_name)
        
def test_search_by_vendor_id(id):
    info_by_id = ven.search_by_vendor_id(id)
    if (len(info_by_id) == 0):
        print("vendor ID (" + id + ") does not exist.")
    else:
        print(info_by_id)
        
def test_search_by_equipment_type(id):
    info_by_equipment = ven.search_by_equipment_type(id)
    if not info_by_equipment:
        print("equipment type (" + id + ") does not exist.")
    else:
        print(info_by_equipment)

ven = EquipmentVendor()


#ven.remove_vendor(1)


#ven.add_vendor("3", "Illumina", "San Diego", "Lab kits", "Preferred")
#ven.add_vendor("4", "Genomatica","San Diego", "Uniform", "Not Preferred")

#ven_name_right = "Illumina"2
#ven_name_wrong = "Amazon"

#test_search_by_vendor_name(ven_name_right)
#test_search_by_vendor_name(ven_name_wrong)

#ven_id_right = "1"
#ven_id_wrong = "5"

#test_search_by_vendor_id(ven_id_right)
#test_search_by_vendor_id(ven_id_wrong)

#ven_equipment_right = "Pharmacy Supplies"
#ven_equipment_wrong = "Xbox"

#test_search_by_equipment_type(ven_equipment_right)
#test_search_by_equipment_type(ven_equipment_wrong)




ven.display_all()


