#!/usr/bin/python3
import tkinter as tk


class HomepageApp:
    def __init__(self, master=None):
        # build ui
        self.homepage_gui = tk.Frame(master)
        self.homepage_gui.configure(borderwidth=0, height=600, width=600)
        self.login_frame = tk.Frame(self.homepage_gui)
        self.login_frame.configure(borderwidth=2, height=100, width=400)
        self.user_label = tk.Label(self.login_frame)
        self.user_label.configure(
            font="{Cascadia Code Light} 12 {}",
            text='Username:')
        self.user_label.grid(column=0, pady=10, row=0, sticky="w")
        self.user_entry = tk.Entry(self.login_frame)
        self.user_entry.configure(
            font="{Cascadia Code Light} 12 {}",
            justify="left",
            takefocus=True,
            width=50)
        self.user_entry.grid(column=0, ipady=5, row=1)
        self.pass_label = tk.Label(self.login_frame)
        self.pass_label.configure(
            cursor="arrow",
            font="{Cascadia Code Light} 12 {}",
            text='Password:')
        self.pass_label.grid(column=0, pady=10, row=2, sticky="w")
        self.pass_entry = tk.Entry(self.login_frame)
        self.pass_entry.configure(
            font="{Cascadia Code Light} 12 {}",
            justify="left",
            show="•",
            takefocus=True,
            validate="none",
            width=50)
        self.pass_entry.grid(column=0, ipady=5, row=3)
        self.login_btn = tk.Button(self.login_frame)
        self.login_btn.configure(
            font="{Cascadia Code Light} 12 {}",
            text='Login')
        self.login_btn.grid(column=0, pady=20, row=4)
        self.login_btn.configure(command=lambda: self.login(self.user_entry.get(), self.pass_entry.get()))
        self.login_frame.pack(pady=100, side="top")
        self.homepage_gui.pack(side="top")
        self.homepage_gui.pack_propagate(0)

        # Main widget
        self.mainwindow = self.homepage_gui

    def run(self):
        self.mainwindow.mainloop()

    def login(self, *args):
        print(f"User: {args[0]}\nPass: {args[1]}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HomepageApp(root)
    app.run()
