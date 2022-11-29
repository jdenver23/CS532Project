from enum import Enum
from pathlib import Path
import os
import csv
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import homepage
import Equipment



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
    
    def search_by_vendor_id(vendor_id):
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




#ven.display_all()

def runGui(user_id):
    
    df = pd.read_csv('EquipmentVendor.csv')
    df.head()
    
    root = tk.Tk()
    root.title("Equipment Vendor")
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
    
    

 

    # NOW add HOME option on top toolbar.
    def return_home():
        root.destroy()
        Equipment.runGui(user_id)
        return

    def search(user_id):
        global tk, entry1
        tk = Tk()
        tk.title('Search equipment vendor database by ID, Vendor name, and equipment type.')
        tk.geometry ("400x200")
        

        label1 = Label(tk,text='Vendor ID').grid(row=0, column=0)
        label2 = Label(tk,text='Vendor name').grid(row=1,column=0)
        label3 = Label(tk,text='Equipment Type').grid(row=2,column=0)
       
        entry1 = Entry(tk)
        entry2 = Entry(tk)
        entry3 = Entry(tk)

        entry1.grid(row=0,column=1)
        entry2.grid(row=1,column=1)
        entry3.grid(row=2,column=1)

        btn1 = Button(tk,text='Search',bg='black',fg='black', command=search_records).grid(row=3,column=1)

        tk.mainloop()
        
    def search_records():
        lookup_record1 = entry1.get()
        tk.destroy()
        for record in tree.get_children():
            tree.delete(record)
                       

        result = EquipmentVendor.search_by_vendor_id(lookup_record1)
        
        tree.insert("", "end", values=list(result.values()))

    def add(user_id):
        tk = Tk()
        tk.title('ADD Equipment Vendor')
        tk.geometry ("400x400")
        label1 = Label(tk,text='Vendor ID').grid(row=0, column=0)
        label2 = Label(tk,text='Vendor Name').grid(row=1,column=0)
        label3 = Label(tk,text='Vendor Address').grid(row=2,column=0)
        label4 = Label(tk,text='Equipment Type').grid(row=3,column=0)
        label5 = Label(tk,text='Preference').grid(row=4,column=0)
       
        entry1 = Entry(tk)
        entry2 = Entry(tk)
        entry3 = Entry(tk)
        entry4 = Entry(tk)
        entry5 = Entry(tk)
      
        
        entry1.grid(row=0,column=1)
        entry2.grid(row=1,column=1)
        entry3.grid(row=2,column=1)
        entry4.grid(row=3,column=1)
        entry5.grid(row=4,column=1)
       
        btn1 = Button(tk,text='ADD',bg='black',fg='black').grid(row=5,column=1)
        tk.mainloop()
        
        
    def delete(user_id):
        tk = Tk()
        tk.title('Delete Equipment Vendor')
        tk.geometry ("400x200")
        label1 = Label(tk,text='Vendor ID').grid(row=0, column=0)
        entry1 = Entry(tk)
        entry1.grid(row=0,column=1)
        btn1 = Button(tk,text='Delete',bg='black',fg='black').grid(row=2,column=1)

        tk.mainloop()
        
    
    def return_add():
        add(user_id)
        root.destroy()
        return
    
    def return_delete():
        delete(user_id)
        root.destroy()
        return        
    
    def return_search_equipment_vendor():
        search(user_id)
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
    
    search_button = tk.Button(top, text= "Search",font=('Verdana', 10),command = return_search_equipment_vendor)
    search_button.grid(row=0, column=3,sticky='ns')    

    exit_button = tk.Button(top, text= "Exit",font=('Verdana', 10),command = root.destroy)
    exit_button.grid(row=0, column=4,sticky='ns')

    root.mainloop()
    
                

if __name__ == "__main__":
    runGui(35280889)





