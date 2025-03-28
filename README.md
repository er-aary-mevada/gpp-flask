# GP Palanpur Institute Portal

A comprehensive web portal for Government Polytechnic Palanpur, built with Flask. This portal serves as both an institutional management system and a collaborative learning platform for students.

## Project Purpose
- Centralized portal for managing institute-wide operations
- Practical learning platform for students to gain real-world development experience
- Collaborative environment for students to contribute features and fixes
- Hands-on experience with modern web development, Git, and team collaboration

## Student Contribution Guide
This project welcomes contributions from EC/ICT/IT department students of GP Palanpur. Here's how to contribute:

1. **Fork the Repository**
   - Visit the repository on GitHub
   - Click the "Fork" button to create your copy

2. **Work on Your Feature**
   - Develop new features or fix bugs in your forked repository
   - Use AI-powered IDEs like Windsurf/Cursor to assist in development
   - Commit your changes regularly with clear commit messages

3. **Testing**
   - Ensure your changes work as intended
   - Test that existing functionality remains unbroken
   - Show your working implementation to Prof. Milav Dabgar

4. **Submit Pull Request**
   - After approval from Prof. Dabgar, create a pull request
   - Clearly describe your changes in the pull request

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
   # Initialize everything (creates database, admin user, sample departments and projects)
   python init_db.py

   # Or initialize specific components:
   python init_db.py --base        # Initialize base database structure only
   python init_db.py --admin       # Create admin user only
   python init_db.py --departments # Create departments only
   python init_db.py --projects    # Create sample projects only

   # You can also combine multiple components:
   python init_db.py --base --admin
   ```
   Default admin credentials:
   - Email: admin@gppalanpur.in
   - Password: admin123

   Note: Please change the admin password after first login.

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

## Feature Status

### Completed Features
- **User Management**
  - Role-based authentication system
  - User registration with approval workflow
  - Bulk user import via CSV
  - Password reset functionality
  - Multi-role support

- **Admin Dashboard**
  - User approval system
  - Department management
  - User creation and management
  - Role assignment

- **Academic Features**
  - Department structure
  - Basic result management system
  - Project tracking system

### In Progress Features
- **Result Management**
  - Semester-wise result upload
  - Result analysis and statistics
  - Individual student result view

- **Department Features**
  - Department-specific announcements
  - Faculty allocation
  - Subject management

### Proposed Features
1. **Academic Management**
   - Attendance tracking system
   - Assignment submission portal
   - Online quiz platform
   - Study material repository
   - Academic calendar management

2. **Library Management**
   - Book inventory system
   - Issue/return tracking
   - Digital library resources
   - Reading list management

3. **Infrastructure**
   - Lab equipment inventory
   - Lab scheduling system
   - Maintenance request system

4. **Student Services**
   - Online fee payment
   - Document request system
   - Grievance submission portal
   - Training and placement portal

5. **Communication**
   - Internal messaging system
   - Notice board with role-based access
   - Event management system
   - Parent portal

6. **Analytics Dashboard**
   - Student performance metrics
   - Attendance analytics
   - Department-wise statistics
   - Placement statistics

### Getting Started with Development
Students interested in contributing can pick any of the proposed features or suggest new ones. Some beginner-friendly starting points:
1. Adding form validation to existing features
2. Improving UI/UX of current pages
3. Adding export functionality for reports
4. Creating new dashboard widgets
5. Implementing notification systems

Remember to:
- Check if someone is already working on your chosen feature
- Break down large features into smaller, manageable tasks
- Follow the contribution guidelines in the section above
- Test thoroughly before submitting pull requests