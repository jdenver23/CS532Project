#This is the Lab Order Tracking subsystem which shall maintain information on all lab tests ordered by physicians for their patients. This is the Backend Component

#Class: CS532 Software Engineering
#Name: Steven Thanhtan Nguyen

import csv #To store our Data
import pandas as pd #For Data Manipulation/Data Access


class LabOrderTracking:

    def backendLabOrderTracking():
    
    #These are the attributes to take care. These are the sample default values for now until they are changed. 

        order_id = 1234 #Any 4 digit value
        patient_name = "Steven" #Can be any String name
        physician_name = "Lindsay" #Can be any String name
        type_labtest = "Blood" #Can be Sugar, Cholestorol, or Both
        date_labtest = "3/17/2022"  #Can be any String date.
        lab_technician = "Michael" #Can be any String name.
        results_labtest = "Good" #Can be good, okay, or urgent

    #Now we get user input if we want to store info in the .CSV file so they can be accessed later
        user_id = input("Please enter your 8 digit USER ID to verify you are an employee.\n")

        if(len(user_id) != 8):
            print("YOU DID NOT ENTER AN 8 digit USER ID. PLEASE TRY AGAIN!!!\n")
            exit()

        first_digit = user_id[0]
        print(first_digit) #Used to test what the first digit of the User ID is. 
    
        if(first_digit != "3"): #Used to make sure only employees access the lab order tracking system
            print("ONLY EMPLOYEES HAVE ACCESS TO THE LAB ORDER TRACKING SYSTEM!!!\n")
            exit() #To stop the program from running if it is not an employee. 

    
        decision = int(input("Please enter 1 for ADDING information to the Lab Order Tracking System, 2 for retrieving SORTED information from the Lab Order Tracking System, or 3 for retrieiving SPECIFIC information from the Lab Order Tracking System. \n")) #If user input == 1, store. If user input == 2, we retrieve. 

    

        if(decision == 1):
            print("We will store information now....")

            decision2 = int(input("Please enter 3 if you want to add to the Main Lab Order Tracking System or 4 if you want to add to the Type of Test Tracking System \n"))

            if(decision2 == 3):


            #We will now ask the user for all the info and then store it into the database FOR THE MAIN LAB ORDER TRACKING SYSTEM 
            #numberofinputs= int("Please enter how many rows of information you will add to the Lab Order Tracking System \n")

                date_labtest = input("Please enter the Date the Lab Test was Performed. Ex. 1/17/2022 \n")
                order_id = input("Please enter the Order ID. Ex. 1234 \n")
                physician_name = input("Please enter the Physician's Name \n").upper()
                patient_name = input("Please enter the Patient's Name \n").upper()
                lab_technician = input("Please enter the Lab Technician's Name \n").upper()
                type_labtest = input("Please enter the Type of Lab Test. Ex. Sugar, Cholesterol, or Both \n").upper()
                results_labtest = input("Please enter the Result of the Lab Test. Ex. Good, Okay, or Urgent \n").upper()
                date_ordered = input("Please enter the Date the Test is Ordered Ex. 1/17/2022 \n")

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
                actual_results = input("Please enter the actual results of the lab test \n")
            

                information_list2 = [order_id2, lab_test_type_id,lab_test_type_name, range_normal_result_values,range_result_values_requiring_immediate_attentionOrUrgentCare, actual_results] #This list is used to store the information before we input it into the .CSV file.
                print (information_list2)

                #Now we store our information in the Type of Test Tracking System. 

                file3 = open('TypeTest.csv', 'a', newline='') #We put newline so we don't skip a line. We put 'a' so we can keep adding to the CSV without overwriting it. 
                writer3 = csv.writer(file3) 
                writer3.writerow(information_list2) #This stores a row of information
                file3.close()


        

    
        


        elif(decision== 2): #This will handle retrieving information from the database now by sorted information.
            print("We will retrieve information now by sorted information....")

            #Ask User if they want to access lab order sorted by "Patient Name", "By Date Ordered", "By Date Performed", or "By Ordering Physician"
            searchingPreference = input("Please enter how you want to acesss the lab orders sorted by. Ex. Normal, Patient Name, By Date Ordered, By Date Performed, Ordering Physician \n").upper() #Add upper since when comparing strings its case sensitive.

            df1 = pd.read_csv("Lab.csv") #Store the CSV as a Dataframe to perform data manipulation like to extract values or change things.
            df2 = pd.read_csv("TypeTest.csv") #Store the CSV as a Dataframe to perform data manipulation like to extract values or change things.

            if(searchingPreference == "NORMAL"): #If the user just wants the data as is. 
                inner_joindfNormal = pd.merge(df1,df2, on = 'Order ID', how = 'inner') #We do an inner join since both tables have same "Order ID".
                print(inner_joindfNormal)
                print("\n")

                #Now we try to find the Urgent Patients to notify the Physicians. 
                print("THIS IS THE LAB TESTS THAT HAVE URGENT RESULTS!!!")
                urgentPatients0 = inner_joindfNormal.query("Result == 'URGENT'")
                print(urgentPatients0)
                print("\n")
                #Now we print out the series/column of those Physicians that are associated with Lab Tests with Urgent in them. 
                print("PLEASE NOTIFY THE FOLLOWING PHYSICIANS!!!")
                print(urgentPatients0['Physician Name'].to_frame().to_string(index=False))

            #df1 = pd.read_csv("Lab.csv") #Store the CSV as a Dataframe to perform data manipulation like to extract values or change things.
            #print(df1)
            #print("\n")

            #df2 = pd.read_csv("TypeTest.csv") #Store the CSV as a Dataframe to perform data manipulation like to extract values or change things.
            #print(df2)

            if(searchingPreference == "PATIENT NAME"): #We will be sorting by the Patient Name in Alphabetical Order Now. 
                print("ORDERED BY PATIENT NAME!!!")


                inner_join_dfPatientName = pd.merge(df1,df2, on = 'Order ID', how = 'inner') #We do an inner join since both tables have same "Order ID". 

                inner_join_dfPatientName = inner_join_dfPatientName.sort_values("Patient Name",ascending = True) #We set ascending to be True so that we increase from A-Z. WORKS!!!!
                inner_join_dfPatientName = inner_join_dfPatientName.dropna() #Everytime we add sometimes it doesn't add right below that row so there's NaN values. 
                print(inner_join_dfPatientName)
                print("\n")
            
                #Now we try to find the Urgent Patients to notify the Physicians. 
                print("THIS IS THE LAB TESTS THAT HAVE URGENT RESULTS!!!")
                urgentPatients1 = inner_join_dfPatientName.query("Result == 'URGENT'")
                print(urgentPatients1)
                print("\n")
                #Now we print out the series/column of those Physicians that are associated with Lab Tests with Urgent in them. 
                print("PLEASE NOTIFY THE FOLLOWING PHYSICIANS!!!")
                print(urgentPatients1['Physician Name'].to_frame().to_string(index=False))
            

            elif (searchingPreference =="BY DATE ORDERED"): #We will be sorting by Date Ordered in Sequential Order Now. WORKS!!!!
                print("ORDERED BY DATE ORDERED!!!")

                inner_join_dfByDateOrdered = pd.merge(df1,df2, on = 'Order ID', how = 'inner') #We do an inner join since both tables have same "Order ID".

                inner_join_dfByDateOrdered = inner_join_dfByDateOrdered.sort_values("Date Ordered",ascending = True)
                inner_join_dfByDateOrdered = inner_join_dfByDateOrdered.dropna()
                print(inner_join_dfByDateOrdered)
                print("\n")

                #Now we try to find the Urgent Patients to notify the Physicians. 
                print("THIS IS THE LAB TESTS THAT HAVE URGENT RESULTS!!!")
                urgentPatients2 = inner_join_dfByDateOrdered.query("Result == 'URGENT'")
                print(urgentPatients2)

                print("\n")
                #Now we print out the series/column of those Physicians that are associated with Lab Tests with Urgent in them. 
                print("PLEASE NOTIFY THE FOLLOWING PHYSICIANS!!!")
                print(urgentPatients2['Physician Name'].to_frame().to_string(index=False))

            elif(searchingPreference =="BY DATE PERFORMED"): #Will be sorting by Date Performed in Sequential Order Now. WORKS!!!!
                print("ORDERED BY DATE PERFORMED!!!")

                inner_join_dfByDatePerformed = pd.merge(df1,df2, on = 'Order ID', how = 'inner') #We do an inner join since both tables have same "Order ID".

                inner_join_dfByDatePerformed  = inner_join_dfByDatePerformed .sort_values("Date of Lab Test",ascending = True)
                inner_join_dfByDatePerformed  = inner_join_dfByDatePerformed .dropna() 
                print(inner_join_dfByDatePerformed)
                print("\n")

                #Now we try to find the Urgent Patients to notify the Physicians. 
                print("THIS IS THE LAB TESTS THAT HAVE URGENT RESULTS!!!")
                urgentPatients3 = inner_join_dfByDatePerformed.query("Result == 'URGENT'")
                print(urgentPatients3)

                print("\n")
                #Now we print out the series/column of those Physicians that are associated with Lab Tests with Urgent in them. 
                print("PLEASE NOTIFY THE FOLLOWING PHYSICIANS!!!")
                print(urgentPatients3['Physician Name'].to_frame().to_string(index=False))



            elif(searchingPreference =="ORDERING PHYSICIAN"): #Will be sorting by Ordering Physician in Alphatical Order Now. WORKS!!!!!
                print("ORDERED BY ORDERING PHYSICIAN!!!")

                inner_join_dfOrderingPhysician = pd.merge(df1,df2, on = 'Order ID', how = 'inner') #We do an inner join since both tables have same "Order ID".
            
                inner_join_dfOrderingPhysician = inner_join_dfOrderingPhysician.sort_values("Physician Name",ascending = True)
                inner_join_dfOrderingPhysician = inner_join_dfOrderingPhysician.dropna() 
                print(inner_join_dfOrderingPhysician)
                print("\n")

                #Now we try to find the Urgent Patients to notify the Physicians. 
                print("THIS IS THE LAB TESTS THAT HAVE URGENT RESULTS!!!")
                urgentPatients4 = inner_join_dfOrderingPhysician.query("Result == 'URGENT'")
                print(urgentPatients4)

                print("\n")
                #Now we print out the series/column of those Physicians that are associated with Lab Tests with Urgent in them. 
                print("PLEASE NOTIFY THE FOLLOWING PHYSICIANS!!!")
                print(urgentPatients4['Physician Name'].to_frame().to_string(index=False))
    
        elif(decision  == 3): #This is for retrieving specific information. 
            df3 = pd.read_csv("Lab.csv") #Store the CSV as a Dataframe to perform data manipulation like to extract values or change things.
            df4 = pd.read_csv("TypeTest.csv") #Store the CSV as a Dataframe to perform data manipulation like to extract values or change things.

            searchingPreference2 = input("Please enter how you want to access specific Lab Reports. Ex. Patient Name, Physician Name, Specific Type Ordered by a Specified Physician, or Specific Type Ordered by all Physicians  \n").upper() #Add upper since when comparing strings its case sensitive.
            #start_time = input("Please enter the start date you would like to see the Lab Orders. Ex. 1/17/2022\n")
            #end_time = input("Please enter the end date you would like to see the Lab Orders. Ex. 1/17/2022\n")

            if(searchingPreference2 == "PATIENT NAME"): #This retrieves information from the database based on the Patient's Name
                print("Retrieiving Information based on PATIENT NAME!!! \n")

            
                PatientNameSearch = input("Please enter the Patient's Name \n").upper()
                #print(PatientNameSearch)

                #Now we retrieve the information based on Patient Name. We need to form an inner join of the tables and then query the data based on that name. 

                inner_join_dfPatientName2 = pd.merge(df3,df4, on = 'Order ID', how = 'inner')
                #print(inner_join_dfPatientName2)
                #Now we use a Boolean Series since .query() method did not work

                #print("\n")
                boolean_series = inner_join_dfPatientName2["Patient Name"] == PatientNameSearch
                #print(boolean_series)

                print(inner_join_dfPatientName2[boolean_series])
        
            elif(searchingPreference2 == "PHYSICIAN NAME"):
                print("Retrieiving Information based on PHYSICIAN NAME!!! \n")

            
                PhysicianNameSearch = input("Please enter the Physician's Name \n").upper()
                #print(PatientNameSearch)

                #Now we retrieve the information based on Patient Name. We need to form an inner join of the tables and then query the data based on that name. 

                inner_join_dfPhysicianName2 = pd.merge(df3,df4, on = 'Order ID', how = 'inner')
                #print(inner_join_dfPatientName2)
                #Now we use a Boolean Series since .query() method did not work

                #print("\n")
                boolean_series = inner_join_dfPhysicianName2["Physician Name"] == PhysicianNameSearch
                #print(boolean_series)

                print(inner_join_dfPhysicianName2[boolean_series])

            elif(searchingPreference2 == "SPECIFIC TYPE ORDERED BY A SPECIFIED PHYSICIAN"):
                print("Retrieiving Information based on SPECIFIC TYPE ORDERED BY A SPECIFIED PHYSICIAN!!! \n")

            
                TypeTestSearch = input("Please enter the specific type of test. Ex. Sugar, Cholesterol, or Both \n").upper()
                PhysicianNameSearch = input("Please enter the Physician's Name \n").upper()
                #print(PatientNameSearch)

                #Now we retrieve the information based on Patient Name. We need to form an inner join of the tables and then query the data based on that name. 

                inner_join_dfTypeTestAndPhysicianName2 = pd.merge(df3,df4, on = 'Order ID', how = 'inner')
                #print(inner_join_dfPatientName2)
                #Now we use a Boolean Series since .query() method did not work

                #print("\n")
                boolean_series = (inner_join_dfTypeTestAndPhysicianName2["Type of Lab Test"] == TypeTestSearch) & (inner_join_dfTypeTestAndPhysicianName2["Physician Name"] == PhysicianNameSearch)
                #print(boolean_series)

                print(inner_join_dfTypeTestAndPhysicianName2[boolean_series])

            elif(searchingPreference2 == "SPECIFIC TYPE ORDERED BY ALL PHYSICIANS"):
                print("Retrieiving Information based on SPECIFIC TYPE ORDERED BY ALL PHYSICIANS!!! \n")

            
                TypeTestSearch = input("Please enter the specific type of test. Ex. Sugar, Cholesterol, or Both \n").upper()
                #print(PatientNameSearch)

                #Now we retrieve the information based on Patient Name. We need to form an inner join of the tables and then query the data based on that name. 

                inner_join_dfTypeTest2 = pd.merge(df3,df4, on = 'Order ID', how = 'inner')
                #print(inner_join_dfPatientName2)
                #Now we use a Boolean Series since .query() method did not work

                #print("\n")
                boolean_series = (inner_join_dfTypeTest2["Type of Lab Test"] == TypeTestSearch)
                #print(boolean_series)

                print(inner_join_dfTypeTest2[boolean_series])





#THIS IS FOR TESTING PURPOSES NOW!!!
    backendLabOrderTracking()     
            



            

            
            
            






    
        


        






    
    
    
    
    
    
    
    
    
    
    #def __init__():
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
    
    