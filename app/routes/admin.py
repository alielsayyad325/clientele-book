from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models.service import Service

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/services")
def list_services():
    services = Service.query.all()
    return render_template("admin/services.html", services=services)

@admin_bp.route("/admin/services/add", methods=["GET", "POST"])
def add_service():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = float(request.form["price"])
        duration = int(request.form["duration"])

        new_service = Service(
            name=name,
            description=description,
            price=price,
            duration_minutes=duration
        )
        db.session.add(new_service)
        db.session.commit()

        return redirect(url_for("admin.list_services"))

    return render_template("admin/add_service.html")
