#This handles the GUI of the Lab Order Tracking System. 

#Class: CS532 Software Engineering
#Name: Steven Thanhtan Nguyen 

#Sources:
# 1. https://www.youtube.com/watch?v=_H5hsUwv8lE&ab_channel=CodingIsFun
# 2. https://www.youtube.com/watch?v=-_z2RPAH0Qk&ab_channel=RealPython
# 3. https://www.geeksforgeeks.org/user-input-in-pysimplegui/
# 4. https://stackoverflow.com/questions/55515627/pysimplegui-call-a-function-when-pressing-button 

import PySimpleGUI as sg
#import LabOrderTracking
#from LabOrderTracking import backendLabOrderTracking





#This is where we create the GUI and try to integrate the backend into it. 
def gui_activation():

    # Add some color
    # to the window
    sg.theme('SandyBeach')     
  
    # Very basic window.
    # Return values using
    # automatic-numbered keys
    layout = [
        [sg.Text('Please enter your 8 digit USER ID:')],
        [sg.Text('User ID Number:', size =(15, 1)), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]
  
    window = sg.Window('Lab Order Tracking System', layout)

    while True:
        event, values = window.read()

        if event == 'Cancel': #If the user presses Cancel, just close the window and do nothing. 
            break
        
        if event == 'Submit': #If the user presses submit, we need to check if the input is valid or not.
            inputHolder = values[0]
            #print(inputHolder)

            if(len(inputHolder) != 8): #Check if User input is 8 digits long before submitting.
                sg.popup("YOU DID NOT ENTER AN 8 digit USER ID.")
                raise SystemExit("Cancelling: User ID Entered was not 8 digits long")
                break
            
            if(inputHolder[0] != "3" and len(inputHolder) == 8): #Used to make sure only employees access the lab order tracking system if the digit code is 8 digits but not start with 3. 
                sg.popup("ONLY EMPLOYEES HAVE ACCESS TO THE LAB ORDER TRACKING SYSTEM!!!\n")
                raise SystemExit("Cancelling: User ID Entered was not valid to access the Lab Order Tracking System")
                break

            if(inputHolder[0] == "3" and len(inputHolder) == 8): #This is where we call our function to get the Lab Order Tracking System Working. 
                sg.popup("NOW GRANTING ACCESS TO THE LAB ORDER TRACKING SYSTEM")
                #LabOrderTracking.backendLabOrderTracking() 








    window.close()
  
    #print(event, values[0])   #Event is what button they pressed. 
    #print(type(event)) #Both buttons are classified as Strings. 



            
     

        
        



#TESTING CODE...........................................................

gui_activation()

