from app import create_app
from app.extensions import db
from app.models.user import User, Role
from flask_security.utils import hash_password
from datetime import datetime

app = create_app()

def create_admin():
    with app.app_context():
        # Get admin role
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            print("Error: Admin role not found. Please run init_db.py first.")
            return

        # Check if admin user exists
        admin_email = 'admin@gppalanpur.in'
        admin_user = User.query.filter_by(email=admin_email).first()
        
        if not admin_user:
            # Create admin user
            admin_user = User(
                email=admin_email,
                password=hash_password('admin123'),  # Default password, please change after first login
                active=True,
                is_approved=True,
                first_name='Admin',
                last_name='User',
                confirmed_at=datetime.utcnow()
            )
            admin_user.roles.append(admin_role)
            
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user created successfully with email: {admin_email}")
            print("Default password: admin123")
        else:
            print("Admin user already exists")

if __name__ == '__main__':
    create_admin()
