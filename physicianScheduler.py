# maintains physician name, employee id, phone number, normal schedule, moving 2 month calendar of appointments
# name, employee id, and phone number can be grabbed from users.csv

# there are 5 physicians: bob mccoy, nola alona, jillian gills, peter mert, steward lettle
# even though there are also 3 physician's assistants and 8 nursing staff, users should not be able to schedule appointments with them

# users can block out time by half hours so we'll assume appointments are half hour
# physicians can also block out half days, days, and weeks

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkcalendar import *
import datetime
import csv

def run_calendar(user_id):
    with open("users.csv", mode = "r") as f:
        reader = csv.reader(f, delimiter = ",")
        for row in reader:
            if row[0] == user_id:
                physician = row[10]

    root = Tk()
    root.title('Physician Scheduler')

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

    today = datetime.datetime.now()
    cal = Calendar(root, selectmode = "day", year = today.year, month = today.month, day = today.day)
    cal.pack(pady = 20)

    def show_appointments():
        return

    show_appt_button = Button(root, text = "Show available appointments")
    show_appt_button.pack(pady = 20)


    # if employee is signed in: show physician name, id, and phone number
    # if patient is signed in: show physician name, and phone number

    root.mainloop()

#run_calendar(90301196)
