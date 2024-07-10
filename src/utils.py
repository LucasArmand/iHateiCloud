import socket
import qrcode
import os
from pillow_heif import register_heif_opener
from PIL import Image

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_ip = None
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip

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
    img.save('resources/qrcode.png')

# Copied from https://github.com/dragonGR/PyHEIC2JPG
def convert_heic_to_jpg(dir):

    # Get all HEIC files in the specified directory
    heic_files = [
        file for file in os.listdir(dir) if file.lower().endswith(".heic")
    ]
    total_files = len(heic_files)

    # Convert each HEIC file to JPG
    num_converted = 0
    for file_index, file_name in enumerate(heic_files, start=1):
        heic_path = os.path.join(dir, file_name)
        jpg_path = os.path.join(dir, os.path.splitext(file_name)[0] + ".jpg")

        try:
            register_heif_opener()
            # Open the HEIC file using pyheif
            with open(heic_path, "rb") as heic_file:
                image = Image.open(heic_file)

            # Save the image as JPG
            with open(jpg_path, "wb") as jpg_file:
                image.save(jpg_file, "JPEG", quality=100)

            os.remove(heic_path)

        except Exception as e:
            print(f"Error converting {file_name}: {str(e)}")