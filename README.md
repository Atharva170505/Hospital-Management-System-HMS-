# Hospital Management System (HMS)

A comprehensive web-based Hospital Management System built with Flask, SQLAlchemy, and Bootstrap that enables efficient management of patients, doctors, appointments, and treatments.

## Features

### Admin Features
- Pre-existing admin account (created programmatically)
- Dashboard with statistics (total doctors, patients, appointments)
- Add, edit, and delete doctor profiles
- Manage patient records
- View all appointments
- Search for doctors by name/specialization
- Search for patients by name/phone

### Doctor Features
- Secure login system
- Dashboard showing today's and upcoming appointments
- View assigned patients
- Mark appointments as completed or cancelled
- Set availability for the next 7 days
- Record diagnosis, prescriptions, and treatment notes
- View patient medical history

### Patient Features
- Self-registration and login
- Dashboard with available departments and doctors
- Search doctors by name or specialization
- Book appointments with available doctors
- Cancel booked appointments
- View appointment history
- Access complete medical history with diagnoses and prescriptions
- Edit profile information

### Core Functionalities
- Prevent double-booking (same doctor, date, time)
- Dynamic appointment status management (Booked → Completed → Cancelled)
- Treatment history tracking
- Department/Specialization management
- REST API endpoints for departments, doctors, and appointments

## Technology Stack

- **Backend:** Flask 3.0.0
- **Database:** SQLite (programmatically created)
- **ORM:** SQLAlchemy
- **Authentication:** Flask-Login
- **Frontend:** HTML5, CSS3, Bootstrap 5.3, Jinja2
- **Icons:** Bootstrap Icons

## Database Schema

### Tables
1. **users** - User authentication (admin, doctor, patient)
2. **departments** - Medical specializations
3. **doctors** - Doctor profiles and details
4. **doctor_availability** - Doctor availability schedule
5. **patients** - Patient profiles and information
6. **appointments** - Appointment bookings
7. **treatments** - Treatment records and prescriptions

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Extract the Project
```bash
cd MAD1Proj
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the Application
```bash
python app.py
```

The application will:
- Create the SQLite database (`hospital.db`)
- Create default departments
- Create an admin user automatically
- Start the development server at `http://127.0.0.1:5000`

## Default Credentials

### Admin Account
- **Email:** admin@hospital.com
- **Password:** admin123

## Project Structure

```
MAD1Proj/
│
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── hospital.db                 # SQLite database (created on first run)
│
├── static/                     # Static files
│   ├── css/                    # Custom CSS files
│   └── js/                     # Custom JavaScript files
│
└── templates/                  # HTML templates
    ├── base.html               # Base template
    ├── index.html              # Landing page
    ├── login.html              # Login page
    ├── register.html           # Patient registration
    │
    ├── admin/                  # Admin templates
    │   ├── dashboard.html
    │   ├── doctors.html
    │   ├── add_doctor.html
    │   ├── edit_doctor.html
    │   ├── patients.html
    │   ├── edit_patient.html
    │   └── appointments.html
    │
    ├── doctor/                 # Doctor templates
    │   ├── dashboard.html
    │   ├── appointments.html
    │   ├── complete_appointment.html
    │   ├── patient_history.html
    │   └── availability.html
    │
    └── patient/                # Patient templates
        ├── dashboard.html
        ├── profile.html
        ├── doctors.html
        ├── book_appointment.html
        ├── appointments.html
        └── history.html
```

## API Endpoints

### GET /api/departments
Get all departments with doctor count

### GET /api/doctors?department_id=<id>
Get all doctors (optionally filtered by department)

### GET /api/appointments/<appointment_id>
Get specific appointment details (requires login)

### GET /api/doctor/<doctor_id>/availability
Get doctor's availability for the next 7 days

## Usage Guide

### For Patients:
1. Register a new account
2. Login with your credentials
3. Search for doctors by name or department
4. Book an appointment with available doctors
5. View your appointments and medical history
6. Update your profile information

### For Doctors:
1. Login with credentials (provided by admin)
2. Set your availability for the week
3. View today's and upcoming appointments
4. Complete appointments and add treatment records
5. View patient medical history

### For Admin:
1. Login with admin credentials
2. Add/edit/delete doctor profiles
3. Manage patient records
4. View all appointments
5. Search for doctors and patients

## Important Notes

- The database is created **programmatically** on the first run
- Admin account is automatically created (no manual registration)
- Doctors are added by admin only
- Patients can self-register
- All forms include validation
- Bootstrap is used for responsive design
- The system prevents appointment conflicts automatically

## Security Features

- Password hashing using Werkzeug's pbkdf2:sha256
- Flask-Login for session management
- Role-based access control
- Protected routes requiring authentication



