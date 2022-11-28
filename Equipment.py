from enum import Enum
from pathlib import Path
import os
import csv
import pandas as pd
import EditPatient
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import homepage
import EquipmentVendor as EV





class Equipment: 
    
    csv_filename = "Equipment.csv"
    field_names = ['Equipment ID', 'Equipment type', 'Equipment description', 'Department', 'Status','Owned','Leased', 'Maintenance History']

    def info(row):
        info_dict = {\
            "Equipment ID": row["Equipment ID"],\
            "Equipment type": row["Equipment type"],\
            "Equipment description" : row["Equipment description"],\
            "Department": row["Department"],\
            "Status": row["Status"],\
            "Owned": row["Owned"],\
            "Leased": row["Leased"],\
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
        
         

    def add_equipment(self, equipment_id, equipment_type, equipment_description, department, Status,Owned,Leased, maintenance_history):

        with open(Equipment.csv_filename, mode = "a", newline = "") as f:
            writer = csv.DictWriter(f, fieldnames=Equipment.field_names)
            writer.writerow({
                "Equipment ID": equipment_id,
                "Equipment type": equipment_type,
                "Equipment description" : equipment_description,
                "Department": department,
                "Status" : Status,
                "Owned" : Owned,
                "Leased" : Leased,
                "Maintenance History" : maintenance_history,
             
            })
        
        print("equipment Added")

  
    # Function for the EQ subsystem shall allow the user to query the equipment equipment information by Equipment ID, Department, and Department.
    
    def search_by_equipment_id(equipment_id):
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


#equip.add_equipment("3", "Wheel Chair", "WC - 205", "Nursing", "Owned","Date Purchase: 08-31-2020 Warranty Serial Number : 0848213","none", "Wheel Fixed")
#equip.add_equipment("4", "PATIENT MONITOR","GT-9000", "Physician", "Owned","Date Purchase: 09-14-2020 Warranty Serial Number : 4568","none", "none")

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

# equip.display_all()


def runGui(user_id):
    
    df = pd.read_csv('Equipment.csv')
    df.head()
    
    root = tk.Tk()
    root.title("Equipment Inventory and Maintenance")
    top = Frame(root)
    bottom = Frame(root)
    top.grid(row=0, column=0)
    bottom.grid(row=1, column=0)
    

    tree = ttk.Treeview(bottom, columns=list(df.columns.values), show='headings')
    tree.grid(row=1, column=0, sticky='nsew')
    
    
    
    y_bar = ttk.Scrollbar(bottom, orient="vertical", command=tree.yview)
    y_bar.grid(row=1, column=1, sticky='ns')
    tree.configure(yscrollcommand=y_bar.set)
    
    for column in tree['column']:
        tree.heading(column,text=column)

    df_rows = df.to_numpy().tolist()
    
    for row in df_rows:
        tree.insert("","end",values=row)


    def return_home():
        root.destroy()
        homepage.home_gui(user_id)
        return
    
    def return_vendor():
        root.destroy()
        EV.runGui(user_id)
        return
    
    def search(user_id):
        global tk, entry1
        tk = Tk()
        tk.title('Search equipment inventory database by ID, and equipment type.')
        tk.geometry ("400x200")
        
        label1 = Label(tk,text='Equipment ID').grid(row=0, column=0)
        label2 = Label(tk,text='Equipment Type').grid(row=1,column=0)

        entry1 = Entry(tk)
        entry2 = Entry(tk)

        entry1.grid(row=0,column=1)
        entry2.grid(row=1,column=1)

        btn1 = Button(tk,text='Search',bg='black',fg='black',command=search_records).grid(row=2,column=1)

        tk.mainloop()
        
    def search_records():
        lookup_record1 = entry1.get()
        tk.destroy()
        for record in tree.get_children():
            tree.delete(record)
                       

        result = Equipment.search_by_equipment_id(lookup_record1)
        
        tree.insert("", "end", values=list(result.values()))


            
        
    def add(user_id):
        tk = Tk()
        tk.title('ADD Equipment')
        tk.geometry ("400x400")
        label1 = Label(tk,text='Equipment ID').grid(row=0, column=0)
        label2 = Label(tk,text='Equipment Type').grid(row=1,column=0)
        label3 = Label(tk,text='Description').grid(row=2,column=0)
        label4 = Label(tk,text='Status').grid(row=3,column=0)
        label5 = Label(tk,text='Owned').grid(row=4,column=0)
        label6 = Label(tk,text='Leased').grid(row=5,column=0)
        label7 = Label(tk,text='Maintenance History').grid(row=6,column=0)
        entry1 = Entry(tk)
        entry2 = Entry(tk)
        entry3 = Entry(tk)
        entry4 = Entry(tk)
        entry5 = Entry(tk)
        entry6 = Entry(tk)
        entry7 = Entry(tk)
        
        entry1.grid(row=0,column=1)
        entry2.grid(row=1,column=1)
        entry3.grid(row=2,column=1)
        entry4.grid(row=3,column=1)
        entry5.grid(row=4,column=1)
        entry6.grid(row=5,column=1)
        entry7.grid(row=6,column=1)
        btn1 = Button(tk,text='ADD',bg='black',fg='black').grid(row=7,column=1)
        tk.mainloop()
        
        
    def delete(user_id):
        global deletetk, entrydelete
        deletetk = Tk()
        deletetk.title('Delete Equipment')
        deletetk.geometry ("400x200")
        label1 = Label(deletetk,text='Equipment ID').grid(row=0, column=0)
        entrydelete = Entry(deletetk)
        entrydelete.grid(row=0,column=1)
        btn1 = Button(deletetk,text='Delete',bg='black',fg='black').grid(row=2,column=1)

        tk.mainloop()

    def delete_records():
        lookup_record2 = entrydelete.get()
        print(lookup_record2)
        deletetk.destroy()
        
    def return_search_equipment():
        search(user_id)
        root.destroy()
        return
    
    def return_add():
        add(user_id)
        root.destroy()
        return
    
    def return_delete():
        delete(user_id)
        root.destroy()
        return
        
        
    
    
    home = tk.Button(top, text= "Home",font=('Verdana', 10),command = return_home)
    home.grid(row=0, column=0,sticky='ns')
    
    add_button = tk.Button(top, text= "Add",font=('Verdana', 10),command = return_add)
    add_button.grid(row=0, column=1,sticky='ns')
    
    delete_button = tk.Button(top, text= "Delete",font=('Verdana', 10),command = return_delete)
    delete_button.grid(row=0, column=2,sticky='ns')
    
    edit_button = tk.Button(top, text= "Edit",font=('Verdana', 10),command = return_home)
    edit_button.grid(row=0, column=3,sticky='ns')
    
    search_button = tk.Button(top, text= "Search",font=('Verdana', 10),command = return_search_equipment)
    search_button.grid(row=0, column=3,sticky='ns')    

    vendors_button = tk.Button(top, text= "List of Vendors",font=('Verdana', 10),command = return_vendor)
    vendors_button.grid(row=0, column=4,sticky='ns')

    exit_button = tk.Button(top, text= "Exit",font=('Verdana', 10),command = root.destroy)
    exit_button.grid(row=0, column=5,sticky='ns')
    
    

    root.mainloop()
    
                

if __name__ == "__main__":
    runGui(35280889)
    
    
    

