from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(email="alielsayyad325@gmail.com").first()
    if user:
        user.role = "admin"
        db.session.commit()
        print(f"User {user.email} promoted to admin!")
    else:
        print("User not found.")
