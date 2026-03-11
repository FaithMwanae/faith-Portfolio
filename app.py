import sqlite3
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "faith_mumo_2026_portfolio_key"

DATABASE = "database.db"

# ==============================
# DATABASE SETUP
# ==============================

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

init_db()


# ==============================
# HOME PAGE
# ==============================

@app.route('/')
def home():
    return render_template("index.html")


# ==============================
# SEND EMAIL FUNCTION
# ==============================

@app.route('/send_email', methods=['POST'])
def send_email():

    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # SAVE MESSAGE TO DATABASE
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO members (name,email,message) VALUES (?,?,?)",
                (name, email, message)
            )

            conn.commit()

    except Exception as e:
        print("Database Error:", e)

    # ==============================
    # EMAIL CONFIGURATION
    # ==============================

    MY_EMAIL = "faithmumo87@gmail.com"

    # PUT YOUR GMAIL APP PASSWORD HERE
    MY_PASS = "ebcg ddgj wfgi opzk"

    msg = MIMEText(
        f"New message from your portfolio website\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n\n"
        f"Message:\n{message}"
    )

    msg["Subject"] = "New Portfolio Contact Message"
    msg["From"] = MY_EMAIL
    msg["To"] = MY_EMAIL

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(MY_EMAIL, MY_PASS)

        server.sendmail(
            MY_EMAIL,
            MY_EMAIL,
            msg.as_string()
        )

        server.quit()

        flash("Message sent successfully!")

    except Exception as e:

        print("SMTP Error:", e)

        flash("Message saved but email failed.")

    return redirect(url_for("home"))


# ==============================
# ADMIN LOGIN
# ==============================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "faith2026":

            session["logged_in"] = True

            return redirect(url_for("admin"))

        else:

            flash("Invalid login credentials")

    return render_template("login.html")


# ==============================
# ADMIN DASHBOARD
# ==============================

@app.route("/admin")
def admin():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        cursor.execute("""
        SELECT id,name,email,message,created_at
        FROM members
        ORDER BY id DESC
        """)

        messages = cursor.fetchall()

    return render_template("admin.html", messages=messages)


# ==============================
# LOGOUT
# ==============================

@app.route("/logout")
def logout():

    session.pop("logged_in", None)

    return redirect(url_for("home"))


# ==============================
# RUN APP
# ==============================

if __name__ == "__main__":
    app.run(debug=True)