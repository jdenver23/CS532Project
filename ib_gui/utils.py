import os
from enum import Enum

base_folder = os.path.dirname(__file__)
def get_icon(icon_file_name):
    return os.path.join(base_folder, f"icons\\{icon_file_name}")

def tk_center(tk, gui_w=None, gui_h=None):
    if gui_w is None:
        gui_w = tk.winfo_width()
    if gui_h is None:
        gui_h = tk.winfo_height()
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()
    
    x = (screen_width/2) - (gui_w/2)
    y = (screen_height/2) - (gui_h/2)
    tk.geometry('%dx%d+%d+%d' % (gui_w, gui_h, x, y))

class UIMode(Enum):
    PATIENT = 0
    EMPLOYEE = 1