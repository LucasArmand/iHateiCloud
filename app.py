from flask import Flask, render_template, request
import os
import qrcode
import threading
import socket

import gui

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.getcwd() + "\\uploads\\"

print(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('upload.html')

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_ip = None
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'File {filename} uploaded successfully!'

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('qrcode.png')
    

if __name__ == '__main__':

    # Generate QR code for local address
    generate_qr_code(f"http://{get_local_ip()}:5000/")

    # Start GUI in a separate thread
    tkinter_thread = threading.Thread(target=gui.GUI, args=([app]))
    tkinter_thread.daemon = True
    tkinter_thread.start()

    # Run Flask app in the main thread
    app.run(host='0.0.0.0')
