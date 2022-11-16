from enum import Enum
from pathlib import Path
import os
import csv
import pandas as pd
from datetime import datetime



class Equipment: 
    
    csv_filename = "Equipment.csv"
    field_names = ['Equipment ID', 'Equipment type', 'Equipment description', 'Department', 'Status', 'Maintenance History']

    def info(row):
        info_dict = {\
            "Equipment ID": row["Equipment ID"],\
            "Equipment type": row["Equipment type"],\
            "Equipment description" : row["Equipment description"],\
            "Department": row["Department"],\
            "Status": row["Status"],\
            "Maintenance History": row["Maintenance History"]    
       }
        return info_dict
        print(info_dict)
 
        
    def display_all(self):
        
        with open('Equipment.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
                
    
    def remove_equipment(self, equipment_id):
        lines = list()
        equipment = input("Please enter a Equipment ID to be deleted.")
        with open('Equipment.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == equipment:
                        lines.remove(row)

        with open('Equipment.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
            
        print ("equipment Removed")  
        
         

    def add_equipment(self, equipment_id, equipment_type, equipment_description, department, Status, maintenance_history):

        with open(Equipment.csv_filename, mode = "a", newline = "") as f:
            writer = csv.DictWriter(f, fieldnames=Equipment.field_names)
            writer.writerow({
                "Equipment ID": equipment_id,
                "Equipment type": equipment_type,
                "Equipment description" : equipment_description,
                "Department": department,
                "Status" : Status,
                "Maintenance History" : maintenance_history,
             
            })
        
        print("equipment Added")

  
    # Function for the EQ subsystem shall allow the user to query the equipment equipment information by Equipment ID, Department, and Department.
    
    def search_by_equipment_id(self, equipment_id):
        with open(Equipment.csv_filename, mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=Equipment.field_names)

            for row in reader:
                if row["Equipment ID"] == equipment_id:
                    information_dictionary = Equipment.info(row)
                    return information_dictionary
            
            return dict()
    
    def search_by_equipment_type(self, equipment_type):
        with open(Equipment.csv_filename,mode = "r", newline = "") as f:
            reader = csv.DictReader(f, fieldnames=Equipment.field_names)

            for row in reader:
                if row["Equipment type"] == equipment_type:
                    information_dictionary = Equipment.info(row)
                    return information_dictionary
            
            return dict()
        





#---------------Testing---------------


        
def test_search_by_equipment_id(id):
    info_by_id = equip.search_by_equipment_id(id)
    if (len(info_by_id) == 0):
        print("Equipment ID (" + id + ") does not exist.")
    else:
        print(info_by_id)
        

def test_search_by_equipment_type(name):
    info_by_type = equip.search_by_equipment_type(name)
    if (len(info_by_type) == 0):
        print("Equipment type (" + name + ") does not exist.")
    else:
        print(info_by_type)
        

equip = Equipment()


#equip.remove_equipment(1)


#equip.add_equipment("3", "Wheel Chair", "WC - 205", "Nursing", "Owned", "Wheel Fixed")
#equip.add_equipment("4", "PATIENT MONITOR","GT-9000", "Physician", "Owned", "none")

#equip_name_right = "Electric Bed"
#equip_name_wrong = "hot dog"

#test_search_by_equipment_type(equip_name_right)
#test_search_by_equipment_type(equip_name_wrong)

#equip_id_right = "2"
#equip_id_wrong = "11"

#test_search_by_equipment_id(equip_id_right)
#test_search_by_equipment_id(equip_id_wrong)

# equip_equipment_right = "Electric Bed"
# equip_equipment_wrong = "Xbox"

# test_search_by_equipment_type(equip_equipment_right)
# test_search_by_equipment_type(equip_equipment_wrong)




equip.display_all()




























































#df = pd.read_csv("Equipment.csv", index_col = 'Equipment ID')
# df = df.drop(df.index[1])
#print(df)
