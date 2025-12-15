# Hospital Management System (HMS)

A comprehensive web-based Hospital Management System built with Flask, designed to streamline hospital operations and manage patients, doctors, appointments, and administrative tasks.

## Features

### Admin Dashboard
- Manage doctors (add, edit, view all doctors)
- Manage patients (view, edit patient information)
- View and manage all appointments
- Department management
- Comprehensive system oversight

### Doctor Portal
- View and manage personal appointments
- Set availability schedules
- Complete appointments and add treatment details
- View patient history and medical records
- Dashboard with appointment statistics

### Patient Portal
- Book appointments with available doctors
- View appointment history
- Manage personal profile
- Browse doctors by department
- Track appointment status

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask session-based authentication
- **Password Security**: Werkzeug password hashing

## Project Structure

```
MAD1Proj/
├── app.py                      # Main application file
├── models/                     # Database models
│   ├── __init__.py
│   ├── user.py                # User model
│   ├── patient.py             # Patient model
│   ├── doctor.py              # Doctor model
│   ├── department.py          # Department model
│   ├── appointment.py         # Appointment model
│   ├── doctor_availability.py # Doctor availability model
│   └── treatment.py           # Treatment model
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin/                 # Admin templates
│   ├── doctor/                # Doctor templates
│   └── patient/               # Patient templates
├── static/                     # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── instance/                   # Database and instance files
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Atharva170505/Hospital-Management-System-HMS-.git
   cd Hospital-Management-System-HMS-
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## Usage

### First Time Setup
1. Register as a new user
2. Login with your credentials
3. Based on your role (Admin/Doctor/Patient), you'll be redirected to the appropriate dashboard

### Default Admin Access
The system creates a default admin account on first run:
- Username: admin
- Password: admin123

**Important**: Change the default admin password after first login for security.

## Database Models

- **User**: Stores user credentials and role information
- **Patient**: Patient personal and medical information
- **Doctor**: Doctor details, specialization, and department
- **Department**: Hospital departments
- **Appointment**: Appointment bookings and status
- **DoctorAvailability**: Doctor schedule and available time slots
- **Treatment**: Treatment records for completed appointments

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control (Admin, Doctor, Patient)
- Protected routes with login requirements

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Atharva - [GitHub Profile](https://github.com/Atharva170505)

## Acknowledgments

- Built as part of Modern Application Development course project
- Flask framework and SQLAlchemy for database management