import os
base_folder = os.path.dirname(__file__)
def get_icon(icon_file_name):
    return os.path.join(base_folder, f"icons\\{icon_file_name}")