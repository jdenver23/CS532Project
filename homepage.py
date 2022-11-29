import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PatientRecords import initialize
import InsuranceBillingGUI
import Equipment
from physicianScheduler import run_calendar

def home_gui(user_id):
    user_id = int(user_id)
    root = Tk()
    root.title('Homepage')

    # width and height
    w = 450
    h = 525

    #------ CENTER FORM ------#
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws - w) / 2
    y = (hs - h) / 2
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))

    mainframe = tk.Frame(root, width = w, height = h)

    def enter_patient_records():
        root.destroy()
        initialize(str(user_id))
        home_gui(str(user_id))

    def enter_physician_scheduler():
        root.destroy()
        run_calendar(str(user_id))

        
    def enter_insurance_billing():
        root.destroy()
        InsuranceBillingGUI.init_gui(str(user_id))
        
    def enter_equipment():
        root.destroy()
        Equipment.runGui(str(user_id))

    #------ ALL BUTTONS -------#
    homeframe  = tk.Frame(mainframe, width = w, height = h)
    home_contentframe = tk.Frame(homeframe, padx = 30, pady = 15, bg = 'grey')

    epr_button = tk.Button(home_contentframe, text = 'Patient Record', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25, command = enter_patient_records)
    sched_button = tk.Button(home_contentframe, text = 'Physician Schedules', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25, command = enter_physician_scheduler)
    lab_button = tk.Button(home_contentframe, text = 'Lab Order Tracking', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25)
    pharm_button = tk.Button(home_contentframe, text = 'Pharmacy Order Tracking', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25)
    insurance_button = tk.Button(home_contentframe, text = 'Insurance Billing', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25, command = enter_insurance_billing)
    equipment_button = tk.Button(home_contentframe, text = 'Equipment Inventory/Maintenance', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25, command =enter_equipment )

    mainframe.pack(fill = 'both', expand = 1)
    homeframe.pack(fill = 'both', expand = 1)
    home_contentframe.pack(fill = 'both', expand = 1)

    epr_button.grid(row = 0, column = 0, columnspan = 2, pady = 5)
    sched_button.grid(row = 1, column = 0, columnspan = 2, pady = 5)
    lab_button.grid(row = 2, column = 0, columnspan = 2, pady = 5)
    pharm_button.grid(row = 3, column = 0, columnspan = 2, pady = 5)
    insurance_button.grid(row = 4, column = 0, columnspan = 2, pady = 5)
    
    if user_id >= 30000000 and user_id < 40000000:
        equipment_button.grid(row = 5, column = 0, columnspan = 2, pady = 5)

    root.mainloop()
