from app import create_app, db
from app.models.appointment import Appointment
from app.models.user import User
from datetime import datetime

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()

    #  Create a sample user (stylist/admin)
    user = User(
        name="Alice Stylist",
        email="alice@example.com"
    )
    user.set_password("securepassword")
    db.session.add(user)
    db.session.commit()

    print("User created:", user)

    # Create a sample appointment
    appt = Appointment(
        client_name="Jane Doe",
        service="Haircut",
        appointment_date=datetime(2025, 7, 15, 14, 0),
        notes="Prefers short layers."
    )
    db.session.add(appt)
    db.session.commit()

    print("Appointments in DB:", Appointment.query.all())
