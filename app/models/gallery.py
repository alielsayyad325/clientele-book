from app import db

class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    description = db.Column(db.Text)
    tags = db.Column(db.String(255))
