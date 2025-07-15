from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db, mail
from app.models.user import User
from app.models.appointment import Appointment
from app.models.service import Service
from flask_mail import Message
from datetime import datetime

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# -------------------------
# Register Route
# -------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))

        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# -------------------------
# Login Route
# -------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


# -------------------------
# Logout Route
# -------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))


# -------------------------
# Forgot Passowrd
# -------------------------
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        # TODO: Validate email, generate token, send email with reset link
        flash("If this email is registered, you’ll receive a password reset link shortly.", "info")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/forgot_password.html")


# -------------------------
# Dashboard Route
# -------------------------
@auth_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "admin":
        return render_template("dashboard.html", name=current_user.name)
    else:
        return redirect(url_for("auth.book"))


# -------------------------
# Booking Route
# -------------------------
@auth_bp.route("/book", methods=["GET", "POST"])
@login_required
def book():
    if current_user.role != "client":
        flash("Only clients can book appointments.")
        return redirect(url_for("auth.dashboard"))

    services = Service.query.all()

    if request.method == "POST":
        service_id = request.form.get("service")
        appointment_date = request.form.get("appointment_date")
        notes = request.form.get("notes")

        service = Service.query.get(service_id)

        if not service:
            flash("Selected service does not exist.", "danger")
            return redirect(url_for("auth.book"))

        new_appt = Appointment(
            client_name=current_user.name,
            service=service.name,
            appointment_date=datetime.strptime(appointment_date, "%Y-%m-%dT%H:%M"),
            notes=notes,
            user_id=current_user.id,
            service_id=service.id
        )

        db.session.add(new_appt)
        db.session.commit()

        # -----------------------------------
        # Send confirmation email to client
        # -----------------------------------
        client_msg = Message(
            subject=f"Your Appointment is Confirmed - {service.name}",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[current_user.email],
            body=f"""Hello {current_user.name},

Thank you for booking with Clientele Book!

Your appointment details:
- Service: {service.name}
- Date/Time: {new_appt.appointment_date.strftime('%Y-%m-%d %I:%M %p')}
- Notes: {notes if notes else 'None'}

We look forward to seeing you!

Best,
Clientele Book Team
"""
        )
        mail.send(client_msg)

        # -----------------------------------
        # Send notification email to admin
        # -----------------------------------
        admin_email = "clientelebookbookings@gmail.com"  # Change to your admin email

        admin_msg = Message(
            subject=f"New Appointment Booked by {current_user.name}",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[admin_email],
            body=f"""Hello Stylist,

A new appointment has been booked:

- Client Name: {current_user.name}
- Client Email: {current_user.email}
- Service: {service.name}
- Date/Time: {new_appt.appointment_date.strftime('%Y-%m-%d %I:%M %p')}
- Notes: {notes if notes else 'None'}

Please check your dashboard for more details.

Best,
Clientele Book System
"""
        )
        mail.send(admin_msg)

        return render_template("booking_success.html", appointment=new_appt)

    return render_template("book.html", services=services)


# -------------------------
# Test Email Route
# -------------------------
@auth_bp.route("/send-test-email")
def send_test_email():
    msg = Message(
        subject="Test Email from Clientele Book",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=["eliasemmanuel948@gmail.com"],
        body="This is a test email sent from Flask-Mail."
    )
    mail.send(msg)
    return "Test email sent!"
