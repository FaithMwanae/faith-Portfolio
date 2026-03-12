from flask import Flask, render_template, request, flash, redirect
import os
import threading
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "mysecretkey")  # secure key

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Contact form route
@app.route("/contact", methods=["POST"])
def contact():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Start email in a background thread so it does not block the request
        threading.Thread(target=send_email, args=(name, email, message)).start()

        flash("Your message has been sent successfully!", "success")
        return redirect("/")
    except Exception as e:
        print("Contact form error:", e)  # logs error
        flash("There was an error sending your message. Please try again later.", "error")
        return redirect("/")

# Safe email sending function
def send_email(name, email, message):
    try:
        smtp_user = os.environ.get("SMTP_USER")
        smtp_password = os.environ.get("SMTP_PASS")
        receiver = os.environ.get("RECEIVER_EMAIL")

        if not smtp_user or not smtp_password or not receiver:
            print("Email environment variables are missing!")
            return

        msg = MIMEText(f"From: {name} <{email}>\n\n{message}")
        msg['Subject'] = "Contact Form Submission"
        msg['From'] = smtp_user
        msg['To'] = receiver

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, receiver, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email sending failed:", e)  # logs error for debugging

# Run the app on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
