from flask import Flask, render_template, send_file
import qrcode
from io import BytesIO
from time import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr')
def generate_qr():
    # Generate QR code
    data = 'Access Granted'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to a BytesIO object
    qr_io = BytesIO()
    qr_img.save(qr_io, 'JPEG')
    qr_io.seek(0)

    # Set expiration time (3 minutes)
    expiration_time = int(time()) + 180

    return send_file(qr_io, mimetype='image/jpeg', as_attachment=True, attachment_filename='access_granted_qr.jpg', cache_timeout=0)

if __name__ == '__main__':
    app.run(debug=True)
