from app import create_app
from app.extensions import db
from app.models.user import User, Role
from flask_security.utils import hash_password
from datetime import datetime

app = create_app()

with app.app_context():
    # Create admin role if it doesn't exist
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Administrator')
        db.session.add(admin_role)
    
    # Create admin user if it doesn't exist
    admin_user = User.query.filter_by(email='admin@gppalanpur.in').first()
    if not admin_user:
        admin_user = User(
            email='admin@gppalanpur.in',
            password=hash_password('admin123'),
            active=True,
            is_approved=True,
            first_name='Admin',
            last_name='User',
            roles=[admin_role]
        )
        db.session.add(admin_user)
    
    db.session.commit()
    print("Admin user created successfully!")
