# Flask Role-Based Authentication Boilerplate

A Flask application template with role-based authentication and user management system.

## Features
- User Authentication (Register, Login, Logout)
- Role-Based Access Control (RBAC)
- Multiple Role Support
- Admin Dashboard
  - User Approval System
  - Single User Creation
  - Bulk User Import via CSV
- Role-Specific Dashboards
- Password Management (Change, Reset)
- Secure Authentication using Flask-Security-Too

## Setup
1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   FLASK_APP=run.py
   FLASK_DEBUG=True
   SECRET_KEY=your-secret-key
   SECURITY_PASSWORD_SALT=your-password-salt
   MAIL_SERVER=smtp.example.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@example.com
   MAIL_PASSWORD=your-email-password
   ```

4. Initialize the database:
   ```
   flask db upgrade
   flask init-db
   ```

5. Run the application:
   ```
   flask run
   ```

## Available Roles
- Admin
- Student
- Lecturer
- Lab Assistant
- HOD
- Librarian
- Principal
- Store Officer

## Sample CSV Format
Check the `sample_data/users.csv` file for the bulk import format.