import csv
from random import randrange
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
import datetime
import homepage


def login_gui():
    root = Tk()

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

    # function will display register frame
    def go_to_register():
        userframe.forget()
        loginframe.forget()
        registerframe.pack(fill = "both", expand = 1)
        root.title('Register')
        # title_label["text"] = 'Register'

    #------ SELECT USER TYPE PAGE ------#
    root.title('Select User Type')
    userframe  = tk.Frame(mainframe, width = w, height = h)
    user_contentframe = tk.Frame(userframe, padx = 30, pady = 100, bg = 'grey')

    message_label = tk.Label(user_contentframe, text = 'Select one of the following:', font = ('Verdana', 16), bg = 'grey')

    radiosframe = tk.Frame(user_contentframe, bg= 'grey')
    account_type = StringVar()
    account_type.set('Patient')
    patient_radiobutton = tk.Radiobutton(radiosframe, text = 'Patient', font = ('Verdana', 14), bg = 'grey', cursor = 'hand2', variable = account_type, value = 'Patient', command = go_to_register)
    employee_radiobutton = tk.Radiobutton(radiosframe, text = 'Employee', font = ('Verdana', 14), bg = 'grey', cursor = 'hand2', variable = account_type, value = 'Employee', command = go_to_register)

    mainframe.pack(fill = 'both', expand = 1)
    userframe.pack(fill = 'both', expand = 1)
    user_contentframe.pack(fill = 'both', expand = 1)

    message_label.grid(row = 0, column = 0, pady = 2, sticky = 'e')
    radiosframe.grid(row = 1, column = 0)
    patient_radiobutton.grid(row = 0, column = 0)
    employee_radiobutton.grid(row = 0, column = 2, padx = 40)

    #------ LOGIN PAGE ------#
    loginframe = tk.Frame(mainframe, width = w, height = h)
    login_contentframe = tk.Frame(loginframe, padx = 30, pady = 100, bg = 'grey')

    # labels
    email_label = tk.Label(login_contentframe, text = 'Email:', font = ('Verdana', 16), bg = 'grey')
    password_label = tk.Label(login_contentframe, text = 'Password:', font = ('Verdana', 16), bg = 'grey')

    # entry boxes
    email_entry = tk.Entry(login_contentframe, font = ('Verdana', 16))
    password_entry = tk.Entry(login_contentframe, font = ('Verdana', 16), show = '*')

    # login button
    login_button = tk.Button(login_contentframe, text = 'Login', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', cursor = 'hand2', padx = 25, pady = 10, width = 25)

    # go to register frame if user doesn't have an account already
    go_register_label = tk.Label(login_contentframe, text = "Don't have an account? Register here", font = ('Verdana', 11, 'bold'), bg = 'grey', fg = '#063970', cursor = 'hand2')

    login_contentframe.pack(fill = 'both', expand = 1)

    # setting up grid for labels, entry boxes, and buttons
    email_label.grid(row = 0, column = 0, pady = 10)
    email_entry.grid(row = 0, column = 1)

    password_label.grid(row = 1, column = 0, pady = 10)
    password_entry.grid(row = 1, column = 1)

    login_button.grid(row = 2, column = 0, columnspan = 2, pady = 40)

    go_register_label.grid(row = 3, column = 0, columnspan = 2, pady = 20)
        
    go_register_label.bind("<Button-1>", lambda page: go_to_register())


    #------ REGISTER PAGE ------#
    registerframe = tk.Frame(mainframe, width = w * 2, height = h)
    register_contentframe = tk.Frame(registerframe, padx = 0, pady = 0, bg = 'grey')

    # labels
    fname_label_rg = tk.Label(register_contentframe, text = 'First Name:', font = ('Verdana', 14), bg = 'grey')
    lname_label_rg = tk.Label(register_contentframe, text = 'Last Name:', font = ('Verdana', 14), bg = 'grey')
    email_label_rg = tk.Label(register_contentframe, text = 'Email:', font = ('Verdana', 14), bg = 'grey')
    password_label_rg = tk.Label(register_contentframe, text = 'Password:', font = ('Verdana', 14), bg = 'grey')
    confirm_password_label_rg = tk.Label(register_contentframe, text = 'Confirm Password:', font = ('Verdana', 14), bg = 'grey')
    phone_label_rg = tk.Label(register_contentframe, text = 'Phone Number:', font = ('Verdana', 14), bg = 'grey')
    address_label_rg = tk.Label(register_contentframe, text = 'Address:', font = ('Verdana', 14), bg = 'grey')
    insurance_carrier_label_rg = tk.Label(register_contentframe, text = 'Insurance:', font = ('Verdana', 14), bg = 'grey')
    dob_label_rg = tk.Label(register_contentframe, text = 'Date of Birth:', font = ('Verdana', 14), bg = 'grey')
    gender_label_rg = tk.Label(register_contentframe, text = 'Gender:', font = ('Verdana', 14), bg = 'grey')

    # entry boxes
    fname_entry_rg = tk.Entry(register_contentframe, font = ('Verdana', 14))
    lname_entry_rg = tk.Entry(register_contentframe, font = ('Verdana', 14))
    email_entry_rg = tk.Entry(register_contentframe, font = ('Verdana', 14))
    password_entry_rg = tk.Entry(register_contentframe, font = ('Verdana', 14), show = '*')
    confirm_password_entry_rg = tk.Entry(register_contentframe, font = ('Verdana', 14), show = '*')
    phone_entry_rg = tk.Entry(register_contentframe, font = ('Verdana', 14))
    address_entry_rg = tk.Entry(register_contentframe, font = ('Verdana', 14))
    insurance_carrier_entry_rg = tk.Entry(register_contentframe, font = ('Verdana', 14))
    dob_entry_rg = tk.Entry(register_contentframe, font = ('Verdana', 14))

    # radiobuttons for gender
    radiosframe = tk.Frame(register_contentframe)
    gender = StringVar()
    gender.set('Male')
    male_radiobutton = tk.Radiobutton(radiosframe, text = 'Male', font = ('Verdana', 14), bg = 'grey', cursor = 'hand2', variable = gender, value = 'Male')
    female_radiobutton = tk.Radiobutton(radiosframe, text = 'Female', font = ('Verdana', 14), bg = 'grey', cursor = 'hand2', variable = gender, value = 'Female')
    other_radiobutton = tk.Radiobutton(radiosframe, text = 'Other', font = ('Verdana', 14), bg = 'grey', cursor = 'hand2', variable = gender, value = 'Other')

    # register button
    register_button = tk.Button(register_contentframe, text = 'Register', font = ('Verdana', 16), bg = '#2980b9', fg = '#fff', cursor = 'hand2', padx = 25, pady = 10, width = 25)

    # takes user to login page if user already has an account set up
    go_login_label = tk.Label(register_contentframe, text = "Already have an account? Login here", font = ('Verdana', 11, 'bold'), bg = 'grey', fg = '#063970', cursor = 'hand2')

    register_contentframe.pack(fill = 'both', expand = 1)

    # setting up grid for labels, entry boxes, and buttons
    fname_label_rg.grid(row = 0, column = 0, pady = 5, sticky = 'e')
    fname_entry_rg.grid(row = 0, column = 1)

    lname_label_rg.grid(row = 1, column = 0, pady = 5, sticky = 'e')
    lname_entry_rg.grid(row = 1, column = 1)

    email_label_rg.grid(row = 2, column = 0, pady = 5, sticky = 'e')
    email_entry_rg.grid(row = 2, column = 1)

    password_label_rg.grid(row = 3, column = 0, pady = 5, sticky = 'e')
    password_entry_rg.grid(row = 3, column = 1)

    confirm_password_label_rg.grid(row = 4, column = 0, pady = 5, sticky = 'e')
    confirm_password_entry_rg.grid(row = 4, column = 1)

    phone_label_rg.grid(row = 5, column = 0, pady = 5, sticky = 'e')
    phone_entry_rg.grid(row = 5, column = 1)

    address_label_rg.grid(row = 6, column = 0, pady = 5, sticky = 'e')
    address_entry_rg.grid(row = 6, column = 1)

    insurance_carrier_label_rg.grid(row = 7, column = 0, pady = 5, sticky = 'e')
    insurance_carrier_entry_rg.grid(row = 7, column = 1)

    dob_label_rg.grid(row = 8, column = 0, pady = 5, sticky = 'e')
    dob_entry_rg.grid(row = 8, column = 1)

    gender_label_rg.grid(row = 9, column = 0, pady = 5, sticky = 'e')
    radiosframe.grid(row = 9, column = 1)
    male_radiobutton.grid(row = 0, column = 0)
    female_radiobutton.grid(row = 0, column = 1)
    other_radiobutton.grid(row = 0, column = 2)

    register_button.grid(row = 10, column = 0, columnspan = 2, pady = 10)

    go_login_label.grid(row = 11, column = 0, columnspan = 2, pady = 5)

    #---------------------------------------------------------------------------------------------------------------#

    # function will display login frame
    def go_to_login():
        registerframe.forget()
        loginframe.pack(fill = "both", expand = 1)
        root.title('Login')
        # title_label["text"] = 'Login'
    # binding the login display function to the label
    go_login_label.bind("<Button-1>", lambda page: go_to_login())

    #------ REGISTER FUNCTION ------#
    def register():
        # saving entries to local variables
        fname = fname_entry_rg.get().strip().upper() # removes white space
        lname = lname_entry_rg.get().strip().upper()
        email = email_entry_rg.get().strip().lower()
        password = password_entry_rg.get().strip()
        confirm_password = confirm_password_entry_rg.get().strip()
        phone = phone_entry_rg.get().strip()
        address = address_entry_rg.get().strip().upper()
        insurance_carrier = insurance_carrier_entry_rg.get().strip().upper()
        dob = dob_entry_rg.get().strip()
        gdr = gender.get()
        account = account_type.get()

        # checking if the fields are filled
        if len(fname) > 0 and len(lname) > 0 and len(email) > 0 and len(password) > 0 and len(confirm_password) > 0 and len(phone) > 0 and len(address) > 0 and len(insurance_carrier) > 0 and len(dob) > 0:
            # checks for valid name
            valid_fname = check_name(fname)
            valid_lname = check_name(lname)
            # checks for a valid email
            valid_email = check_email(email)
            # generate id number based on account type
            id = make_id(account)
            # check for valid phone number
            valid_phone = check_phone_num(phone)
            # check if passwords match
            valid_pass = passwords_match(password, confirm_password)
            valid_dob = check_dob(dob)
            if valid_fname and valid_lname and valid_email and valid_phone and valid_pass and valid_dob:
                with open("C:/Users/linds/OneDrive/Documents/GitHub/CS532Project/users.csv", mode = "a", newline = "") as f:
                    writer = csv.writer(f, delimiter = ",")
                    # make sure passwords match and then input all information to csv file/database of users
                    # displays a warning message if they don't match
                    rand_physician = randrange(1,6)
                    physician = assign_physician(rand_physician)
                    writer.writerow([id, fname, lname, email, password, phone, address, insurance_carrier, dob, gdr, physician])
                    messagebox.showinfo('Register', 'Your account has been created successfully and you can now log in. Here is your ID Number: ' + str(id) + '. Make sure to save it for any future use.')
                    go_to_login()
        # if it makes it here, there is at least one empty field
        else:
            messagebox.showwarning('Register', 'Please try again, make sure all fields are filled.')

    # function to make sure that only letters are being entered in the first and last name entry boxes
    def check_name(name_entered):
        if name_entered.isalpha():
            return True
        else:
            messagebox.showwarning('Register', 'Please only put letters in your name.')
            return False

    # function to check for a valid email (contains @****.com)
    def check_email(email_entered):
        invalid_email = True
        new_email = True
        while(invalid_email and new_email):
            with open("C:/Users/linds/OneDrive/Documents/GitHub/CS532Project/users.csv", mode = "r") as f:
                reader = csv.reader(f, delimiter = ",")
                # this checks if email is already in use by another account
                for row in reader:
                    if row[3] == email_entered:
                        new_email = False
                        messagebox.showwarning('Register', 'This email has been registered to an account already. Please log in instead.')
                        go_to_login()
                        return False
            if "@gmail.com" in email_entered or "@yahoo.com" in email_entered or "@hotmail.com" in email_entered or "@aol.com" in email_entered or "@comcast.net" in email_entered and new_email:
                invalid_email = False
                return True
            else:
                messagebox.showwarning('Register', "Invalid email. Please enter a 'gmail', 'yahoo', 'hotmail', 'aol', or 'comcast' email.")
                break

    # function to generate id number
    def make_id(acc_type):
        while True:
            id_number = 0
            # employees will have an id number that starts with a 300-399 number
            if acc_type == "Employee":
                id_number = randrange(30000000, 40000000)
            # patients will have an id number that starts with a 400-999 number
            else:
                id_number = randrange(40000000, 100000000)
            num_found = False
            with open("C:/Users/linds/OneDrive/Documents/GitHub/CS532Project/users.csv", mode = "r") as f:
                reader = csv.reader(f, delimiter = ",")
                # this checks if the id number is already in use
                # if it is, it will go through the loop again and generate a new one
                for row in reader:
                    if(row[0] == id_number):
                        num_found = True
                if num_found == False:
                    break
        return id_number

    # function to check if passwords match and is at least 8 characters
    def passwords_match(pass1, pass2):
        if pass1 == pass2:
            return True
        elif len(pass1) < 8:
            messagebox.showwarning('Register', 'Your password needs to be at least 8 characters long.')
        else:
            messagebox.showwarning('Register', 'Your passwords do not match.')

    # function to check for a valid phone number (10 digits)
    def check_phone_num(phone_num_entered):
        if len(phone_num_entered) == 10 and phone_num_entered.isnumeric():
            return True
        else:
            messagebox.showwarning('Register', 'Please enter a valid US phone number, starting with the area code.')

    # function to check for a valid dob (mm/dd/yyyy format)
    def check_dob(dob_entered):
        try:
            datetime.datetime.strptime(dob_entered, "%m/%d/%Y")
            return True
        except:
            messagebox.showwarning('Register', 'Please enter your date of birth in MM/DD/YYYY format.')

    def assign_physician(num):
        match num:
            case 1:
                return "BOB MCCOY"
            case 2:
                return "NOLA ALONA"
            case 3:
                return "JILLIAN GILLS"
            case 4:
                return "PETER MERT"
            case 5:
                return "STEWARD LETTLE"

    # clicking the register button will run the register function
    register_button['command'] = register

    #------ LOGIN FUNCTION ------#
    def validate_login():
        email_in = email_entry.get().strip().lower()
        password_in = password_entry.get().strip()
        if len(email_in) > 0 and len(password_in) > 0:
            with open("C:/Users/linds/OneDrive/Documents/GitHub/CS532Project/users.csv", mode = "r") as f:
                reader = csv.reader(f, delimiter = ",")
                # checks for email/password combo in database
                for row in reader:
                    if email_in in row[3] and password_in in row[4]:
                        # get id from row here
                        id = row[0]
                        messagebox.showinfo('Login', 'Login successful.')
                        # take to homepage after logging in
                        root.destroy()
                        homepage.home_gui(id)
                    elif row[3] == email_in and row[4] != password_in:
                        messagebox.showinfo('Login', 'Incorrect password, please try again.')
                messagebox.showinfo('Login', 'That email does not exist, please register for an account.')
                go_to_register()
        else:
            messagebox.showwarning('Login', 'Please fill all fields.')
    
    login_button['command'] = validate_login

    root.mainloop()

if __name__ == "__main__":
    # only run the code below when executed as script
    # this prevents auto code executions from being imported as a module
    login_gui()