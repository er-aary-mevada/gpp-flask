from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from .extensions import db, mail, csrf, bootstrap, migrate, security
from .models.user import User, Role
from .models.department import Department
from .models.project import Project
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)

    # Setup Flask-Security
    from .forms.auth import LoginForm
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore,
                     login_form=LoginForm)

    # Register blueprints
    from .routes.main import bp as main_bp
    from .routes.auth import bp as auth_bp
    from .routes.admin import bp as admin_bp
    from .routes.dashboard import bp as dashboard_bp
    from .routes.student import bp as student_bp
    from .routes.ssip import bp as ssip_bp
    from .routes.ssip_coordinator import bp as ssip_coordinator_bp
    from .routes.student_services import bp as student_services_bp
    from .filters import bp as filters_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(ssip_bp, url_prefix='/ssip')
    app.register_blueprint(ssip_coordinator_bp, url_prefix='/ssip-coordinator')
    app.register_blueprint(student_services_bp, url_prefix='/student-services')
    app.register_blueprint(filters_bp)

    return app
