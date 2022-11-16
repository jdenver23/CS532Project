import tkinter as tk


class SeperatorContainerWidget(tk.Frame):
    def __init__(self, master=None, **kw):
        super(SeperatorContainerWidget, self).__init__(master, **kw)
        self.line_seperator = tk.LabelFrame(self)
        self.line_seperator.configure(height=2, width=200)
        self.line_seperator.pack(
            anchor="center",
            expand="true",
            fill="x",
            padx=10,
            side="left")
        self.configure(height=4, width=720)
        self.pack_propagate(0)