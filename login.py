import csv
from random import randrange

def register():
    #need first name, mi, last name, email, and create password
    with open("users.csv", mode = "a", newline = "") as f:
        writer = csv.writer(f, delimiter = ",")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        while True:
            id_number = randrange(30000000, 100000000)
            num_found = False
            with open("users.csv", mode = "r") as f:
                reader = csv.reader(f, delimiter = ",")
                for row in reader:
                    if(row[0] == id_number):
                        num_found = True
                if num_found == False:
                    break
        invalid_email = True
        while(invalid_email):
            email = input("Enter your email: ")
            if "@gmail.com" in email or "@yahoo.com" in email or "@hotmail.com" in email or "@aol.com" in email:
                invalid_email = False
            else:
                print("Invalid email. Please enter a 'gmail', 'yahoo', 'hotmail', or 'aol' email.")
        while True:
            password = input("Enter a password: ")
            password2 = input("Re-enter the password: ")
            if password == password2:
                writer.writerow([id_number, first_name, last_name, email, password])
                print("You are now registered. This is your ID number: " + str(id_number))
                break
            else:
                print("Passwords do not match, please try again")
        #generate IDs --> patient vs. employee?


def login():
    while True:
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        with open("users.csv", mode = "r") as f:
            reader = csv.reader(f, delimiter = ",")
            for row in reader:
                if row[3] == email and row[4] == password:
                    print("Successful login")
                    return True
        print("Email and/or password are incorrect, please try again")

register()
login()