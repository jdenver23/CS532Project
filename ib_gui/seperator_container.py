#!/usr/bin/env python
import tkinter as tk


class SeperatorContainerWidget(tk.Frame):
    def __init__(self, master=None, show=True, **kw):
        super(SeperatorContainerWidget, self).__init__(master, **kw)
        self.line_seperator = tk.LabelFrame(self)
        self.line_seperator.configure(height=2, width=200)
        self.line_seperator.pack(
            anchor="center",
            expand="true",
            fill="x",
            padx=10,
            side="left")
        self.configure(height=4, width=960)
        if not show: self.configure(height=0)
        self.pack_propagate(0)
        
if __name__ == "__main__":
    root = tk.Tk()
    widget = SeperatorContainerWidget(root)
    # widget.pack(expand=True, fill="both")
    root.mainloop()

