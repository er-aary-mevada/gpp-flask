from app import create_app
from app.extensions import db
from app.models.user import User, Role
from app.models.department import Department

app = create_app()

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default roles if they don't exist
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator')
            db.session.add(admin_role)
        
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user', description='Regular User')
            db.session.add(user_role)
        
        # Create default department if it doesn't exist
        default_dept = Department.query.filter_by(name='General').first()
        if not default_dept:
            default_dept = Department(name='General')
            db.session.add(default_dept)
        
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
