from genericpath import isfile
import tkinter as tk #Create GUI
from tkinter import filedialog, Text #Help us pick the apps (filedialog). Help us us display text (Text)
import os #Help us run apps on app.



root = tk.Tk() #Body that holds entire app. Attach buttons/frame to the root.

apps = []  #Array/List of all the apps we opened up before. 

#Outputs whatever we read from the file. 
if os.path.isfile('save.txt'): 
    with open('save.txt', 'r') as f:
        tempApps = f.read()
        tempApps = tempApps.split(',')
        apps = [x for x in tempApps if x.strip()]

def addApp():

    for widget in frame.winfo_children(): #Used to remove duplicates on file locations
        widget.destroy()

    #Only access executable files. 
    filename = filedialog.askopenfilename(initialdir="/", title = "Select File", filetypes = (("executables","*.exe"),("all files", "*.*"))) #*.exe means all files that have .exe extension to it.  

    apps.append(filename)
    print(filename)
    for app in apps: #Get all the apps and attach it to the screen (the location of the app)
        label = tk.Label(frame, text=app, bg= "gray")
        label.pack()

def runApps(): #It actually opens up the apps and runs them. 
    for app in apps:
        os.startfile(app)

canvas = tk.Canvas(root,height = 700, width = 700, bg = "#263D42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth = 0.8, relheight = 0.8, relx = 0.1, rely = 0.1) #Relx, Rely helps space the white box in the middle. 

#Add some buttons

openFile = tk.Button(root,text = "Open File", padx = 10, pady = 5, fg = "white", bg = "#263D42", command = addApp) #Creates an Open File Button
openFile.pack() #Puts the Button on the Root. 


runApps= tk.Button(root,text = "Run Apps", padx = 10, pady = 5, fg = "white", bg = "#263D42",command = runApps ) #Creates an Open File Button

runApps.pack() 

for app in apps:
    label = tk.Label(frame, text= app)
    label.pack()

root.mainloop() 

with open('save.txt', 'w') as f: #"w" means write. Everytime we close our app, we will save a .txt file and write that .txt file. The save.txt file keeps track of the apps that were open.
    for app in apps:
        f.write(app + ',')
