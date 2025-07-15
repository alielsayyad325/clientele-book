from datetime import datetime
from app import db
from sqlalchemy import Enum
import enum


class AppointmentStatus(enum.Enum):
    pending = "Pending"
    confirmed = "Confirmed"
    declined = "Declined"
    cancelled = "Cancelled"
    completed = "Completed"
    no_show = "No-Show"
    break_time = "Break/Unavailable"


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client_profiles.id"), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=True)

    stylist_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    title = db.Column(db.String(120), nullable=True)  # Optional: for calendar titles
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    status = db.Column(Enum(AppointmentStatus), default=AppointmentStatus.pending, nullable=False)

    notes = db.Column(db.Text, nullable=True)  # Admin/stylist notes
    client_notes = db.Column(db.Text, nullable=True)  # Optional client input

    reschedule_reason = db.Column(db.String(255), nullable=True)
    cancellation_reason = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client = db.relationship("ClientProfile", backref="appointments", lazy=True)
    service = db.relationship("Service", backref="appointments", lazy=True)
    stylist = db.relationship("User", backref="stylist_appointments", lazy=True)

    def is_past(self):
        return self.end_time < datetime.utcnow()

    def is_active(self):
        return self.status in [AppointmentStatus.pending, AppointmentStatus.confirmed]

    def __repr__(self):
        return f"<Appointment {self.id} - {self.status.value}>"    
