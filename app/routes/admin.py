from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.models.service import Service
from app.models.appointment import Appointment
from app.utils.decorators import admin_required
from app import db

# Use a url_prefix to avoid repeating /admin in every route
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# -----------------------------
# List Services
# -----------------------------
@admin_bp.route("/services")
@login_required
@admin_required
def list_services():
    services = Service.query.all()
    return render_template("admin/services.html", services=services)

# -----------------------------
# Add Service
# -----------------------------
@admin_bp.route("/services/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_service():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        duration = request.form["duration"]

        new_service = Service(
            name=name,
            description=description,
            price=float(price),
            duration_minutes=int(duration)
        )
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for("admin.list_services"))

    return render_template("admin/add_service.html")

# -----------------------------
# Edit Service
# -----------------------------
@admin_bp.route("/services/edit/<int:service_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)

    if request.method == "POST":
        service.name = request.form["name"]
        service.description = request.form["description"]
        service.price = float(request.form["price"])
        service.duration_minutes = int(request.form["duration"])
        db.session.commit()
        return redirect(url_for("admin.list_services"))

    return render_template("admin/edit_service.html", service=service)

# -----------------------------
# Delete Service
# -----------------------------
@admin_bp.route("/services/delete/<int:service_id>", methods=["POST"])
@login_required
@admin_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for("admin.list_services"))

# -----------------------------
# View Appointments
# -----------------------------
@admin_bp.route("/appointments")
@login_required
@admin_required
def view_appointments():
    appointments = Appointment.query.order_by(Appointment.start_time).all()
    return render_template("admin/appointments.html", appointments=appointments)
