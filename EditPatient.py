import csv
import tkinter as tk
import PatientRecords
import pandas as pd
from tkinter import *

#GUI for edit records using tkinter
def runGui(id_number):
    top = tk.Tk()

    top.title("Edit Patient Record")

    top.geometry("300x300")

    def exit_entry():
        top.destroy()
        PatientRecords.initialize(id_number)

    exit_button = tk.Button(top, text='Back', command = exit_entry)
    exit_button.grid(row=0, column=0, pady=5)
    
    first_name_var=tk.StringVar()
    last_name_var=tk.StringVar()
    email_var = tk.StringVar()
    phone_var=tk.StringVar()
    address_var=tk.StringVar()

    #Once needed, can submit changes and writes to csv
    def submit():
        df = pd.read_csv('users.csv')
        for r in df.index:
            if(df["ID"][r].astype(str) == id_number):
                if(first_name_var.get() != ""):
                    df.at[r, "First Name"] = first_name_var.get().strip().upper()
                if(last_name_var.get() != ""):
                    df.at[r, "Last Name"] = last_name_var.get().strip().upper()
                if(email_var.get() != ""):
                    df.at[r, "Email"] = email_var.get().strip().lower()
                if(phone_var.get() != ""):
                    df.at[r, "Phone Number"] = phone_var.get()
                if(address_var.get() != ""):
                    df.at[r, "Address"] = address_var.get()
        df.to_csv("users.csv", index=False)

    first_name_label = tk.Label(top, text = 'First Name', font=('calibre',10, 'bold'))
    first_name_entry = tk.Entry(top, textvariable = first_name_var, font=('calibre',10,'normal'))
    
    last_name_label = tk.Label(top, text = 'Last Name', font = ('calibre',10,'bold'))
    last_name_entry=tk.Entry(top, textvariable = last_name_var, font = ('calibre',10,'normal'))

    email_label = tk.Label(top, text = 'Email', font = ('calibre',10,'bold'))
    email_entry=tk.Entry(top, textvariable = email_var, font = ('calibre',10,'normal'))

    phone_label = tk.Label(top, text = 'Phone Number', font =('calibre',10, 'bold'))
    phone_entry = tk.Entry(top, textvariable = phone_var, font =('calibre',10,'normal'))
    
    address_label = tk.Label(top, text = 'Address', font = ('calibre',10,'bold'))
    address_entry=tk.Entry(top, textvariable = address_var, font = ('calibre',10,'normal'))
    
    sub_btn=tk.Button(top,text = 'Submit', command = submit)
    
    first_name_label.grid(row = 1, column = 0, pady = 5)
    first_name_entry.grid(row = 1, column = 1, pady = 5)

    last_name_label.grid(row = 2, column = 0, pady = 5)
    last_name_entry.grid(row = 2, column = 1, pady = 5)

    email_label.grid(row = 3, column = 0, pady = 5)
    email_entry.grid(row = 3, column = 1, pady = 5)

    phone_label.grid(row = 4, column = 0, pady = 5)
    phone_entry.grid(row = 4, column = 1, pady = 5)

    address_label.grid(row = 5, column = 0, pady = 5)
    address_entry.grid(row = 5, column = 1, pady = 5)
    
    sub_btn.grid(row = 6, column = 0, pady = 5)

    top.mainloop()

#Main entry to GUI
def enter_prog(passed_id_number):
    with open("users.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0] == passed_id_number:
                runGui(row[0])