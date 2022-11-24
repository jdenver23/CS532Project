#This handles the GUI of the Lab Order Tracking System. 

#Class: CS532 Software Engineering
#Name: Steven Thanhtan Nguyen 

#Sources:
# 1. https://www.youtube.com/watch?v=_H5hsUwv8lE&ab_channel=CodingIsFun

import PySimpleGUI as sg
#import LabOrderTracking
#from LabOrderTracking import backendLabOrderTracking




#This is where we create the GUI and try to integrate the backend into it. 
def gui_activation():
    text = sg.popup_get_text("Please enter your 8 digit USER ID:")
    #print(type(text)) Used to check what data type the input is. It is classifed as a String. 
    if not text: #This is good to make sure the user inputs numbers or else nothing happens. 
        sg.popup("              Cancel", "No numbers were entered")
        raise SystemExit("Cancelling: no numbers entered")
    
    #If the user input numbers, we can check if it is valid then run our function. 
    else: 
        sg.popup("You have entered",text)

        if(len(text) != 8):
            sg.popup("YOU DID NOT ENTER AN 8 digit USER ID. PLEASE TRY AGAIN!!!")
            raise SystemExit("Cancelling: User ID Entered was not 8 digits long")

        first_digit = text[0]
        #print(first_digit) #Used to test what the first digit of the User ID is. 
    
        if(first_digit != "3"): #Used to make sure only employees access the lab order tracking system
            sg.popup("ONLY EMPLOYEES HAVE ACCESS TO THE LAB ORDER TRACKING SYSTEM!!!\n")
            raise SystemExit("Cancelling: User ID Entered was not valid to access the Lab Order Tracking System")

        if(first_digit == "3"): #This is where we call our function to get the Lab Order Tracking System Working. 
            sg.popup("NOW GRANTING ACCESS TO THE LAB ORDER TRACKING SYSTEM")
            
        

        
        



#TESTING CODE...........................................................

gui_activation()

