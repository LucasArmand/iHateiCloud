from flask import Flask, render_template, request
import os
import threading

import config
import gui
import utils

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist("files")
    for file in files:
        filename = file.filename
        print(f"saving {filename}")
        file.save(os.path.join(app.config['upload_path'], filename))
    utils.convert_heic_to_jpg(app.config["upload_path"])
    
    return "Files uploaded successfully"


if __name__ == '__main__':

    # Set default upload directory if none set
    if "upload_path" not in config.get_settings_obj().keys():
        config.write_setting("upload_path", f"{os.getcwd()}\\uploads\\")
    
    # Configure Flask app upload path
    app.config["upload_path"] = config.get_settings_obj()["upload_path"]

    # Generate QR code for local address
    utils.generate_qr_code(f"http://{utils.get_local_ip()}:5000/")

    # Start GUI in a separate thread to stop Flask app blocking
    tkinter_thread = threading.Thread(target=gui.GUI, args=([app]))
    tkinter_thread.daemon = True
    tkinter_thread.start()

    # Run Flask app in the main thread
    app.run(host='0.0.0.0')
