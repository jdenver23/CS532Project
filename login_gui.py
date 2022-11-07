import tkinter as tk
from tkinter import filedialog, Text, mainloop
import os

root = tk.Tk()
apps = []

def add_app():
    for widget in frame.winfo_children():
        widget.destroy()
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("executables", "*.exe"), ("all files", "*.*")))
    apps.append(filename)
    print(filename)
    for app in apps:
        label = tk.Label(frame, text = app, bg = "gray")
        label.pack()

def run_apps():
    for app in apps:
        os.startfile(app)

canvas = tk.Canvas(root, height = 600, width = 600, bg = "#263D42")
canvas.pack()

frame = tk.Frame(root, bg = "white")
frame.place(relwidth = 0.7, relheight = 0.7, relx = 0.15, rely = 0.1)

open_file = tk.Button(root, text = "Open file", padx = 10, pady = 5, fg = "white", bg = "#263D42", command = add_app)
open_file.pack()

run_apps = tk.Button(root, text = "Run apps", padx = 10, pady = 5, fg = "white", bg = "#263D42", command = run_apps)
run_apps.pack()

root = mainloop()

with open('save.txt', 'w') as f:
    for app in apps:
        f.write(app + ',')