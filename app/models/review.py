from app import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
