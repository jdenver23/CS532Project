import tkinter as tk
from utils import get_icon

class NavbarContainerWidget(tk.Frame):
    def __init__(self, master=None, **kw):
        super(NavbarContainerWidget, self).__init__(master, **kw)
        self.left_seperator = tk.Label(self)
        self.left_seperator.configure(justify="left")
        self.left_seperator.pack(anchor="w", side="left")
        self.btn_home = tk.Button(self)
        self.img_home = tk.PhotoImage(file=get_icon("home.png"))
        self.btn_home.configure(
            activebackground="#2980b9",
            borderwidth=0,
            image=self.img_home,
            justify="left",
            overrelief="flat",
            relief="flat")
        self.btn_home.pack(anchor="w", ipadx=5, padx=5, pady=10, side="left")
        self.btn_save_changes = tk.Button(self)
        self.img_save = tk.PhotoImage(file=get_icon("save.png"))
        self.btn_save_changes.configure(
            activebackground="#2980b9",
            borderwidth=0,
            image=self.img_save,
            overrelief="flat",
            relief="flat")
        self.btn_save_changes.pack(
            anchor="w", ipadx=5, padx=5, pady=10, side="left")
        self.btn_undo_change = tk.Button(self)
        self.img_undo = tk.PhotoImage(file=get_icon("undo.png"))
        self.btn_undo_change.configure(
            activebackground="#2980b9",
            borderwidth=0,
            image=self.img_undo,
            justify="left",
            overrelief="flat",
            relief="flat")
        self.btn_undo_change.pack(
            anchor="w",
            ipadx=5,
            padx=5,
            pady=10,
            side="left")
        self.right_seperator = tk.Label(self)
        self.right_seperator.configure(justify="left")
        self.right_seperator.pack(anchor="e", side="right")
        self.btn_logout = tk.Button(self)
        self.img_logout = tk.PhotoImage(file=get_icon("logout.png"))
        self.btn_logout.configure(
            activebackground="#2980b9",
            borderwidth=0,
            image=self.img_logout,
            justify="left",
            overrelief="flat",
            relief="flat")
        self.btn_logout.pack(
            anchor="e",
            ipadx=5,
            padx=5,
            pady=10,
            side="right")
        self.line_seperator = tk.LabelFrame(self)
        self.line_seperator.configure(height=2, width=200)
        self.line_seperator.pack(
            anchor="e",
            expand="true",
            fill="x",
            padx=5,
            side="top")
        self.configure(height=50, width=720)
        self.pack_propagate(0)