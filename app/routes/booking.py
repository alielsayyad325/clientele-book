from flask import Blueprint, render_template

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/book")
def booking_page():
    return render_template("booking.html")
