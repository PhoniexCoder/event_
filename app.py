from flask import Flask, request, jsonify
import qrcode
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

app = Flask(__name__)

@app.route("/send_email", methods=["POST"])
def send_email():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    # Generate unique ID
    unique_id = f"EVENT-{data.get('row')}-{int(io.time.time())}"

    # Generate QR code
    qr = qrcode.make(unique_id)
    img_byte = io.BytesIO()
    qr.save(img_byte, format="PNG")
    img_byte.seek(0)

    # Email setup
    msg = MIMEMultipart("related")
    msg["Subject"] = "Your Attendance QR – technIEEEks’ 25"
    msg["From"] = os.environ.get("EMAIL_USER")
    msg["To"] = email

    html = f"""
    <p>Dear <b>{name}</b>,</p>
    <p>Please find your unique QR code below:</p>
    <img src="cid:qrcode">
    <p>Bring this QR on event day for check-in.</p>
    <p>Best Regards,<br>IEEE SB GEHU</p>
    """

    msg.attach(MIMEText(html, "html"))

    img = MIMEImage(img_byte.read())
    img.add_header("Content-ID", "<qrcode>")
    msg.attach(img)

    # SMTP (example using Gmail)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASSWORD"))
        server.sendmail(os.environ.get("EMAIL_USER"), email, msg.as_string())

    return jsonify({"status": "success", "email": email})

if __name__ == "__main__":
    app.run(debug=True)