import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory
import os
import sys
import config

class GUI:
    def __init__(self, app):
        self.app = app

        self.root = tk.Tk()
        self.root.title("iHateiCloud")

        self.root.minsize(1000, 0)

        qr_code = Image.open("resources/qrcode.png")
        photo = ImageTk.PhotoImage(qr_code)


        # Set the icon
        self.root.iconbitmap(f"{os.getcwd()}\\resources\\icon.ico")

        # 
        self.upload_path_label = tk.Label(self.root, text=f"{app.config['upload_path']}", font=('Arial', 24))
        self.upload_path_label.pack()

        self.qr_code = tk.Label(self.root, image=photo)
        self.qr_code.image = photo
        self.qr_code.pack(fill=tk.BOTH, expand=tk.YES)

        self.upload_location_btn = tk.Button(self.root, text="Select Upload Location", font=("Arial", 24), command=self.upload_location_dialog)
        self.upload_location_btn.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def on_closing(self):
        os._exit(1) # Kill app

    def upload_location_dialog(self):
        path = askdirectory()
        check = self.is_valid_path(path)
        if check[0]:
            config.write_setting("upload_path", path)        # Update settings
            self.app.config["upload_path"] = path            # Update Flask upload path
            self.upload_path_label.config(text=f"{path}")    # Update GUI text
        else:
            self.upload_path_label.config(text=f"{check[1]}") 
        

    def is_valid_path(self, path):

        if not os.path.exists(path):
            return False, "Path does not exist."
        
        if not os.path.isdir(path):
            return False, "Path is not a directory."
        
        if not os.access(path, os.R_OK | os.W_OK):
            return False, "Insufficient permissions for the directory."
        
        restricted_paths = ['/etc', '/bin', '/usr/bin', '/var', 'C:/Windows', 'C:/Program Files']
        if any(path.startswith(restricted_path) for restricted_path in restricted_paths):
            return False, "Path points to a restricted directory."
        
        return True, "Path is valid."


