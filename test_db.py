from app import create_app, db
from app.models.appointment import Appointment
from app.models.user import User
from app.models.service import Service
from app.models.client_profile import ClientProfile
from app.models.review import Review
from app.models.gallery import GalleryImage
from datetime import datetime

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()

    # Create a sample user (stylist/admin)
    user = User(
        name="Alice Stylist",
        email="alice@example.com"
    )
    user.set_password("securepassword")
    db.session.add(user)
    db.session.commit()

    print("User created:", user)

    # Create a sample service
    service = Service(
        name="Haircut",
        description="Professional haircut service.",
        price=45.00,
        duration_minutes=45
    )
    db.session.add(service)
    db.session.commit()

    print("Service created:", service)

    # Create a sample client profile
    client_profile = ClientProfile(
        user_id=user.id,
        notes="Prefers short layers and is allergic to certain products."
    )
    db.session.add(client_profile)
    db.session.commit()

    print("Client profile created:", client_profile)

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

    # Create a sample review
    review = Review(
        user_id=user.id,
        appointment_id=appt.id,
        rating=5,
        comment="Excellent service, very happy with my haircut!"
    )
    db.session.add(review)
    db.session.commit()

    print("Review created:", review)

    # Create a sample gallery image
    gallery_image = GalleryImage(
        filename="before_after.jpg",
        description="Before and after of a haircut.",
        tags="haircut, style, transformation"
    )
    db.session.add(gallery_image)
    db.session.commit()

    print("Gallery image created:", gallery_image)

    # Print all data
    print("All Services:", Service.query.all())
    print("All Client Profiles:", ClientProfile.query.all())
    print("All Reviews:", Review.query.all())
    print("All Gallery Images:", GalleryImage.query.all())
