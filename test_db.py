from app import create_app, db
from app.models.appointment import Appointment
from datetime import datetime

app = create_app()

with app.app_context():
    db.create_all()

    appt = Appointment(
        client_name="Jane Doe",
        service="Haircut",
        appointment_date=datetime(2025, 7, 15, 14, 0),
        notes="Prefers short layers."
    )
    db.session.add(appt)
    db.session.commit()

   
    print(Appointment.query.all())
