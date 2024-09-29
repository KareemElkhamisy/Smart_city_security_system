from flask import Flask, render_template, request, redirect, url_for
import qrcode
import base64
import threading
from io import BytesIO


app = Flask(__name__)

users = {
    "1": "1234"  #  one user 
}

# Dictionary to store QR code data
qr_data = {}

#  generate QR code
def generate_qr(data):
    qr = qrcode.make(data)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    buffered.seek(0)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


#clear QR code data 
def clear_qr_data():
    global qr_data
    threading.Timer(180.0, lambda: qr_data.pop("qr_code", None)).start()

# Login page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        home_number = request.form["home_number"]
        password = request.form["password"]
        if home_number in users and users[home_number] == password:
            return redirect(url_for("qr_generator"))
        else:
            return render_template("login.html", message="Invalid home number or password.")
    return render_template("login.html", message="")

# QR page
@app.route("/qr_generator", methods=["GET", "POST"])
def qr_generator():
    if request.method == "POST":
        data = "Access granted"
        qr_data["qr_code"] = data
        #call clear QR
        clear_qr_data()
        return render_template("qr_generator.html", qr_data=generate_qr(data))
    return render_template("qr_generator.html", qr_data="")

if __name__ == "__main__":
    app.run(debug=True)
