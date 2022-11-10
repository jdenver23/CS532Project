#This is the Lab Order Tracking subsystem which shall maintain information on all lab tests ordered by physicians for their patients.

#Class: CS532 Software Engineering
#Name: Steven Thanhtan Nguyen

import csv #To store our Data
import pandas as pd #For Data Manipulation/Data Access


class LabOrderTracking:
    
    #These are the attributes to take care. These are the sample default values for now until they are changed. 

    order_id = 1234 #Any 4 digit value
    patient_name = "Steven" #Can be any String name
    physician_name = "Lindsay" #Can be any String name
    type_labtest = "Blood" #Can be Sugar, Cholestorol, or Both
    date_labtest = "3/17/2022"  #Can be any String date.
    lab_technician = "Michael" #Can be any String name.
    results_labtest = "Good" #Can be good, okay, or urgent

    #Now we get user input if we want to store info in the .CSV file so they can be accessed later
    decision = int(input("Please enter 1 for adding information to the Lab Order Tracking System and 2 for retrieving information from the Lab Order Tracking System \n")) #If user input == 1, store. If user input == 2, we retrieve. 

    if(decision == 1):
        print("We will store information now....")

        decision2 = int(input("Please enter 3 if you want to add to the Main Lab Order Tracking System or 4 if you want to add to the Type of Test Tracking System \n"))

        if(decision2 == 3):


        #We will now ask the user for all the info and then store it into the database FOR THE MAIN LAB ORDER TRACKING SYSTEM 
        #numberofinputs= int("Please enter how many rows of information you will add to the Lab Order Tracking System \n")

            date_labtest = input("Please enter the Date the Lab Test was Performed. Ex. 2022-01-17 \n")
            order_id = input("Please enter the Order ID. Ex. 1234 \n")
            physician_name = input("Please enter the Physician's Name \n").upper()
            patient_name = input("Please enter the Patient's Name \n").upper()
            lab_technician = input("Please enter the Lab Technician's Name \n").upper()
            type_labtest = input("Please enter the Type of Lab Test. Ex. Sugar, Cholesterol, or Both \n").upper()
            results_labtest = input("Please enter the Result of the Lab Test. Ex. Good, Okay, or Urgent \n").upper()
            date_ordered = input("Please enter the Date the Test is Ordered Ex. 2022-01-17 \n")

            information_list = [date_labtest,order_id,physician_name,patient_name,lab_technician,type_labtest,results_labtest,date_ordered ] #This list is used to store the information before we input it into the .CSV file.
            print (information_list)
        
        
            #This is for Testing Purposes. 
            #print(order_id)
            #print(patient_name)
            #print(physician_name)
            #print(type_labtest)
            #print(date_labtest)
            #print(lab_technician)
            #print(results_labtest)
            #print(date_ordered)
            #Now we write to the CSV file to store the information. 
        
            field_names = ["Date of Lab Test","Order ID","Physician Name","Patient Name","Lab Technician","Type of Lab Test", "Result", "Date Test is Ordered"]
 

            #This is to store information now. 
            file2 = open('Lab.csv', 'a', newline='') #We put newline so we don't skip a line. We put 'a' so we can keep adding to the CSV without overwriting it. 
            writer2 = csv.writer(file2) 
            writer2.writerow(information_list) #This stores a row of information
            file2.close()
        
        elif(decision2 == 4): #This handles if we want to add to the Type of Test Tracking System.
            order_id2 = input("Please enter the Order ID. Ex. 1234 \n")
            lab_test_type_id = input("Please enter the Lab Test Type ID. Ex.1234 \n")
            lab_test_type_name = input("Please enter the Lab Test Type Name Ex. Sugar,Cholesterol, or Both \n").upper()
            range_normal_result_values = input("Please enter the Range of Normal Result Values. Ex.[0-100] \n")
            range_result_values_requiring_immediate_attentionOrUrgentCare = input("Please enter the Range Result Values Requiring Immediate Attention or Urgent Care \n")
            

            information_list2 = [order_id2, lab_test_type_id,lab_test_type_name, range_normal_result_values,range_result_values_requiring_immediate_attentionOrUrgentCare] #This list is used to store the information before we input it into the .CSV file.
            print (information_list2)

            #Now we store our information in the Type of Test Tracking System. 

            file3 = open('TypeTest.csv', 'a', newline='') #We put newline so we don't skip a line. We put 'a' so we can keep adding to the CSV without overwriting it. 
            writer3 = csv.writer(file3) 
            writer3.writerow(information_list2) #This stores a row of information
            file3.close()


        


        


    else: #This will handle retrieving information from the database now. 
        print("We will retrieve information now....")

        #Ask User if they want to access lab order by "Patient Name", "By Date Ordered", "By Date Performed", or "By Ordering Physician"
        searchingPreference = input("Please enter how you want to acesss the lab orders. Ex. Patient Name, By Date Ordered, By Date Performed, Ordering Physician \n").upper() #Add upper since when comparing strings its case sensitive.


        df1 = pd.read_csv("Lab.csv") #Store the CSV as a Dataframe to perform data manipulation like to extract values or change things.
        print(df1)
        print("\n")

        df2 = pd.read_csv("TypeTest.csv") #Store the CSV as a Dataframe to perform data manipulation like to extract values or change things.
        print(df2)

        if(searchingPreference == "PATIENT NAME"): #We will be sorting by the Patient Name in Alphabetical Order Now. 
            print("ORDERED BY PATIENT NAME!!!")


            inner_join_dfPatientName = pd.merge(df1,df2, on = 'Order ID', how = 'inner') #We do an inner join since both tables have same "Order ID". 

            inner_join_dfPatientName = inner_join_dfPatientName.sort_values("Patient Name",ascending = True) #We set ascending to be True so that we increase from A-Z. WORKS!!!!
            inner_join_dfPatientName = inner_join_dfPatientName.dropna() #Everytime we add sometimes it doesn't add right below that row so there's NaN values. 
            print(inner_join_dfPatientName)

        elif (searchingPreference =="BY DATE ORDERED"): #We will be sorting by Date Ordered in Sequential Order Now. WORKS!!!!
            print("ORDERED BY DATE ORDERED!!!")

            inner_join_dfByDateOrdered = pd.merge(df1,df2, on = 'Order ID', how = 'inner') #We do an inner join since both tables have same "Order ID".

            inner_join_dfByDateOrdered = inner_join_dfByDateOrdered.sort_values("Date Ordered",ascending = True)
            inner_join_dfByDateOrdered = inner_join_dfByDateOrdered.dropna()
            print(inner_join_dfByDateOrdered)

        elif(searchingPreference =="BY DATE PERFORMED"): #Will be sorting by Date Performed in Sequential Order Now. WORKS!!!!
            print("ORDERED BY DATE PERFORMED!!!")

            inner_join_dfByDatePerformed = pd.merge(df1,df2, on = 'Order ID', how = 'inner') #We do an inner join since both tables have same "Order ID".

            inner_join_dfByDatePerformed  = inner_join_dfByDatePerformed .sort_values("Date of Lab Test",ascending = True)
            inner_join_dfByDatePerformed  = inner_join_dfByDatePerformed .dropna() 
            print(inner_join_dfByDatePerformed)

        elif(searchingPreference =="ORDERING PHYSICIAN"): #Will be sorting by Ordering Physician in Alphatical Order Now. WORKS!!!!!
            print("ORDERED BY ORDERING PHYSICIAN!!!")

            inner_join_dfOrderingPhysician = pd.merge(df1,df2, on = 'Order ID', how = 'inner') #We do an inner join since both tables have same "Order ID".
            
            inner_join_dfOrderingPhysician = inner_join_dfOrderingPhysician.sort_values("Physician Name",ascending = True)
            inner_join_dfOrderingPhysician = inner_join_dfOrderingPhysician.dropna() 
            print(inner_join_dfOrderingPhysician)


        






    
    
    
    
    
    
    
    
    
    
    def __init__():
        #self.order_id = order_id
        #self.patient_name = patient_name
        #self.physician_name = physician_name
        #self.type_labtest = type_labtest
        #self.date_labtest= date_labtest
        #self.lab_technician = lab_technician
        #self.results_labtest = results_labtest

        #For "By Date Ordered" & "By Ordering Physician"
        #self.date_ordered = date_ordered
        #self.ordering_physician = ordering_physician


    #self,order_id, patient_name, physician_name, type_labtest, date_labtest,lab_technician, results_labtest,date_ordered, ordering_physician ADD THIS BACK INTO CONSTRUCTOR ARGUMENT IF NECESSARY
    
    # Accessor Methods for our Attributes
        def get_order_id(self):
            return self.order_id
    
        def get_patient_name(self):
            return self.patient_name
    
        def get_physician_name(self):
            return self.physician_name
   
        def get_type_labtest(self):
            return self.type_labtest
    
        def get_date_labtest(self):
            return self.date_labtest
    
        def get_lab_technician(self):
            return self.lab_technician
    
        def get_results_labtest(self):
            return self.results_labtest

        def get_date_ordered(self):
            return self.date_ordered

        def get_ordering_physician(self):

            return self.ordering_physician

    # Mutator Methods for our Attributes

        def set_order_id(self,new_order_id):
            self.order_id = new_order_id
    
        def set_patient_name(self,new_patient_name):
            self.patient_name = new_patient_name
    
        def set_physician_name (self,new_physician_name ):
            self.physician_name  = new_physician_name 
    
        def set_type_labtest(self,new_type_labtest):
            self.type_labtest = new_type_labtest 
    
        def set_date_labtest(self,new_date_labtest):
            self.date_labtest = new_date_labtest
    
        def set_lab_technician(self,new_lab_technician):
            self.lab_technician = new_lab_technician
    
        def set_results_labtest(self,new_results_labtest):
            self.results_labtest= new_results_labtest

        def set_date_ordered(self,new_date_ordered):
            self.date_ordered = new_date_ordered
        
        def set_ordering_physician(self,new_ordering_physician):
         self.ordering_physician = new_ordering_physician
    