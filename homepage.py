import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import PatientRecords
from PatientRecords import initialize

def home_gui(user_id):
    user_id = int(user_id)
    root = Tk()

    # width and height
    w = 450
    h = 525

    #------ CENTER FORM ------#
    root.overrideredirect(1) # removes border
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws - w) / 2
    y = (hs - h) / 2
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))

    #------ HEADER ------#
    headerframe = tk.Frame(root, width = w, height = 50)
    titleframe = tk.Frame(headerframe, padx = 1, pady = 1)
    title_label = tk.Label(titleframe, text = 'Home Page', padx = 20, pady = 5, font = ('Tahoma', 24))
    close_button = tk.Button(headerframe, text = 'x', borderwidth = 1, relief = 'solid', font = ('Vaerdana', 12), bg = 'red')

    headerframe.pack()
    titleframe.pack()
    title_label.pack()
    close_button.pack()

    titleframe.place(rely = 0.5, relx = 0.5, anchor = CENTER)
    close_button.place(x = 410, y = 10)

    # closing the window
    def close_window():
        headerframe.forget()
        root.destroy()

    close_button['command'] = close_window
    #------ END HEADER ------#

    mainframe = tk.Frame(root, width = w, height = h)

    #------ ALL BUTTONS -------#
    homeframe  = tk.Frame(mainframe, width = w, height = h)
    home_contentframe = tk.Frame(homeframe, padx = 30, pady = 15, bg = 'grey')

    epr_button = tk.Button(home_contentframe, text = 'Patient Record', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25)
    sched_button = tk.Button(home_contentframe, text = 'Physician Schedules', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25)
    lab_button = tk.Button(home_contentframe, text = 'Lab Order Tracking', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25)
    pharm_button = tk.Button(home_contentframe, text = 'Pharmacy Order Tracking', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25)
    insurance_button = tk.Button(home_contentframe, text = 'Insurance Billing', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25)
    equipment_button = tk.Button(home_contentframe, text = 'Equipment Inventory/Maintenance', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', padx = 25, pady = 10, width = 25)

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

    epr_button['command'] = initialize(user_id)

    root.mainloop()
