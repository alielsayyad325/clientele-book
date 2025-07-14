from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clientele.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "supersecretkey"
    app.debug = True

    
    # This is the app's official sending email account.
    #
    # For example:
    #    bookings@clientelebook.com
    #    noreply@clientelebook.com
    #
    # All outgoing emails will come from here,
    # but we can customize the "From Name"
    # for each stylist in our email logic.
    #
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "clientelebookbookings@gmail.com"
    app.config["MAIL_PASSWORD"] = "knrj sclg rdmz sznh"

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # ---------------------------------------------------
    # Import the models
    # ---------------------------------------------------
    from app.models import (
        appointment,
        user,
        service,
        client_profile,
        review,
        gallery
    )

    # ---------------------------------------------------
    # Register blueprints
    # ---------------------------------------------------
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.booking import booking_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(booking_bp)

    # ---------------------------------------------------
    # User loader for Flask-Login
    # ---------------------------------------------------
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # ---------------------------------------------------
    # Handle 403 errors gracefully
    # ---------------------------------------------------
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    return app
