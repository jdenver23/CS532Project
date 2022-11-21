import tkinter as tk
from tkinter import messagebox
from .utils import get_icon
import homepage
import login
import sys

# add .. to import from above top level package
sys.path.append("..")

class NavbarContainerWidget(tk.Frame):
    def __init__(self, bill, master=None, **kw):
        super(NavbarContainerWidget, self).__init__(master, **kw)
        self.bill = bill
        self.master = master
        
        self.seperator_0 = tk.Label(self)
        self.seperator_0.configure(relief="flat")
        self.seperator_0.pack(anchor="w", side="left", padx=5)
        
        self.btn_home = tk.Button(self)
        self.img_home = tk.PhotoImage(file=get_icon("home.png"))
        self.btn_home.configure(
            borderwidth=0,
            image=self.img_home,
            justify="left",
            overrelief="flat",
            relief="flat",
            command=self.home)
        self.btn_home.pack(anchor="w", padx=5, pady=5, side="left")
        self.btn_home.bind("<Enter>", self.btn_on_mouse_enter, add="+")
        self.btn_home.bind("<Leave>", self.btn_on_mouse_leave, add="+")
        self.btn_save_changes = tk.Button(self)
        self.img_save = tk.PhotoImage(file=get_icon("save.png"))
        self.btn_save_changes.configure(
            borderwidth=0,
            image=self.img_save,
            overrelief="flat",
            relief="flat",
            command=self.save_changes)
        self.btn_save_changes.pack(
            anchor="w", ipadx=1, padx=10, pady=5, side="left")
        self.btn_save_changes.bind("<Enter>", self.btn_on_mouse_enter, add="+")
        self.btn_save_changes.bind("<Leave>", self.btn_on_mouse_leave, add="+")
        
        self.btn_pull_db = tk.Button(self)
        self.img_pull = tk.PhotoImage(file=get_icon("pull.png"))
        self.btn_pull_db.configure(
            borderwidth=0,
            image=self.img_pull,
            justify="left",
            overrelief="flat",
            relief="flat",
            command=self.pull_db)
        self.btn_pull_db.pack(
            anchor="w",
            ipadx=2,
            padx=5,
            pady=5,
            side="left")
        self.btn_pull_db.bind("<Enter>", self.btn_on_mouse_enter, add="+")
        self.btn_pull_db.bind("<Leave>", self.btn_on_mouse_leave, add="+")
        
        self.seperator_1 = tk.Label(self)
        self.seperator_1.configure(relief="flat")
        self.seperator_1.pack(anchor="e", side="right", padx=5)
        
        self.btn_logout = tk.Button(self)
        self.img_logout = tk.PhotoImage(file=get_icon("logout.png"))
        self.btn_logout.configure(
            borderwidth=0,
            image=self.img_logout,
            justify="left",
            overrelief="flat",
            relief="flat",
            command=self.logout)
        self.btn_logout.pack(anchor="e", padx=5, pady=5, side="right")
        self.btn_logout.bind("<Enter>", self.btn_on_mouse_enter, add="+")
        self.btn_logout.bind("<Leave>", self.btn_on_mouse_leave, add="+")
        self.configure(height=75, width=960)
        self.pack_propagate(0)
        
        self.line_selector = tk.LabelFrame(self)
        self.line_selector.configure(height=2, width=36)
        
        self.tooltip_selector = tk.Label(self)
        self.tooltip_selector.configure(font="{Verdana} 8 {}")
        
        self.master.bind("<Control_L>s", lambda x: self.save_changes())
    
    def pull_db(self):
        if messagebox.askyesno("Pull data from database", "Do you want pull data from database and discard all changes?"):
            ddc = self.master.calls(widget_name="ddc")
            ddc.pull_from_db()
            messagebox.showinfo("Save Changes", "Successful!")
    
    def save_changes(self):
        if messagebox.askyesno("Save Changes", "Do you want to commit changes to database?"):
            self.bill.commit_to_db()
            messagebox.showinfo("Save Changes", "Successful!")
        
    def home(self):
        if messagebox.askyesno("Home", "Are you sure you want to go to home?"):
            self.master.destroy()
            homepage.home_gui(self.bill.user['ID'])
    
    def logout(self):
        if messagebox.askyesno("Log out", "Are you sure you want to log out?"):
            self.master.destroy()
            login.login_gui()

    def btn_on_mouse_enter(self, event=None):
        _text = "Home"
        tt_dx = -2
        tt_dy = 34
        ls_dx = 0
        ls_dy = 33
        if event.widget == self.btn_save_changes:
            _text = "Save"
            ls_dx -= 3
            tt_dx -= 1
        elif event.widget == self.btn_pull_db:
            _text = "Pull"
            tt_dx += 5
            ls_dx -= 2
        elif event.widget == self.btn_logout:
            _text = 'Log out'
            ls_dx -= 3
            tt_dx -= 7
            
        self.tooltip_selector.configure(text=_text)
        self.tooltip_selector.place(x=event.widget.winfo_x()+tt_dx, y=event.widget.winfo_y()+tt_dy)
        self.tooltip_selector.lift()
        self.line_selector.place(x=event.widget.winfo_x()+ls_dx, y=event.widget.winfo_y()+ls_dy)
        self.line_selector.lift()
        # event.widget['background'] = '#dadada'
        

    def btn_on_mouse_leave(self, event=None):
        self.line_selector.place_forget()
        self.tooltip_selector.place_forget()
        # event.widget['background'] = 'SystemButtonFace' #default button color


if __name__ == "__main__":
    root = tk.Tk()
    widget = NavbarContainerWidget(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
