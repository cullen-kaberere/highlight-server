from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# -------------------------------
# Configure email from .env
# -------------------------------
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "True") == "True"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    studentGrade = data.get("studentGrade", "")
    inquiryType = data.get("inquiryType", "")
    message = data.get("message", "")

    body = f"""
    New message from website contact form:

    Name: {name}
    Email: {email}
    Phone: {phone}
    Grade: {studentGrade}
    Inquiry Type: {inquiryType}

    Message:
    {message}
    """

    msg = Message(
        subject=f"New Contact Form Message from {name}",
        recipients=[os.getenv("MAIL_USERNAME")],  # receive at your own email
        body=body
    )

    try:
        mail.send(msg)
        return jsonify({"success": True, "message": "Message sent successfully!"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
