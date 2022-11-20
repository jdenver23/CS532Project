import tkinter as tk
from .utils import get_icon

class NavbarContainerWidget(tk.Frame):
    def __init__(self, master=None, **kw):
        super(NavbarContainerWidget, self).__init__(master, **kw)
        
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
            relief="flat")
        self.btn_home.pack(anchor="w", padx=5, pady=5, side="left")
        self.btn_home.bind("<Enter>", self.btn_on_mouse_enter, add="+")
        self.btn_home.bind("<Leave>", self.btn_on_mouse_leave, add="+")
        self.btn_save_changes = tk.Button(self)
        self.img_save = tk.PhotoImage(file=get_icon("save.png"))
        self.btn_save_changes.configure(
            borderwidth=0,
            image=self.img_save,
            overrelief="flat",
            relief="flat")
        self.btn_save_changes.pack(
            anchor="w", ipadx=1, padx=10, pady=5, side="left")
        self.btn_save_changes.bind("<Enter>", self.btn_on_mouse_enter, add="+")
        self.btn_save_changes.bind("<Leave>", self.btn_on_mouse_leave, add="+")
        self.btn_undo_change = tk.Button(self)
        self.img_undo = tk.PhotoImage(file=get_icon("undo.png"))
        self.btn_undo_change.configure(
            borderwidth=0,
            image=self.img_undo,
            justify="left",
            overrelief="flat",
            relief="flat")
        self.btn_undo_change.pack(
            anchor="w",
            ipadx=2,
            padx=5,
            pady=5,
            side="left")
        self.btn_undo_change.bind("<Enter>", self.btn_on_mouse_enter, add="+")
        self.btn_undo_change.bind("<Leave>", self.btn_on_mouse_leave, add="+")
        
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
            relief="flat")
        self.btn_logout.pack(anchor="e", padx=5, pady=5, side="right")
        self.btn_logout.bind("<Enter>", self.btn_on_mouse_enter, add="+")
        self.btn_logout.bind("<Leave>", self.btn_on_mouse_leave, add="+")
        self.configure(height=70, width=960)
        self.pack_propagate(0)
        
        self.line_selector = tk.LabelFrame(self)
        self.line_selector.configure(height=2, width=36)
        
        self.tooltip_selector = tk.Label(self)
        self.tooltip_selector.configure(font="{Verdana} 8 {}")
        

    def btn_on_mouse_enter(self, event=None):
        _text = "Home"
        tt_dx = -2
        tt_dy = 34
        if event.widget == self.btn_save_changes:
            _text = "Save"
            tt_dx = 0
        elif event.widget == self.btn_undo_change:
            _text = "Undo"
            tt_dx = 0
        elif event.widget == self.btn_logout:
            _text = 'Logout'
            tt_dx = -5
            
        self.tooltip_selector.configure(text=_text)
        self.tooltip_selector.place(x=event.widget.winfo_x()+tt_dx, y=event.widget.winfo_y()+tt_dy)
        
        self.line_selector.place(x=event.widget.winfo_x(), y=event.widget.winfo_y()+33)
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
