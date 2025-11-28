# Models Package

This package contains all database models for the Hospital Management System.

## Structure

Each model is defined in its own file for better organization and maintainability:

- **`__init__.py`** - Initializes the database and imports all models
- **`user.py`** - User model (authentication and authorization)
- **`department.py`** - Department/Specialization model
- **`doctor.py`** - Doctor model
- **`doctor_availability.py`** - Doctor availability schedule model
- **`patient.py`** - Patient model
- **`appointment.py`** - Appointment booking model
- **`treatment.py`** - Treatment record model

## Database Schema

### User
- Base authentication model for all users (admin, doctor, patient)
- Relationships: 1:1 with Doctor or Patient

### Department
- Medical specializations (Cardiology, Neurology, etc.)
- Relationships: 1:N with Doctors

### Doctor
- Doctor profile and information
- Relationships: N:1 with Department, 1:N with Appointments, 1:N with DoctorAvailability

### DoctorAvailability
- Doctor's available time slots
- Relationships: N:1 with Doctor

### Patient
- Patient profile and information
- Relationships: 1:N with Appointments

### Appointment
- Appointment bookings between patients and doctors
- Relationships: N:1 with Patient, N:1 with Doctor, 1:1 with Treatment

### Treatment
- Medical treatment records for completed appointments
- Relationships: 1:1 with Appointment

## Usage

Import models in your application:

```python
from models import db, User, Doctor, Patient, Appointment, Treatment, Department, DoctorAvailability
```

Or import specific models:

```python
from models.user import User
from models.doctor import Doctor
from models.patient import Patient
```

## Database Initialization

The database is initialized in `app.py`:

```python
from models import db

app = Flask(__name__)
db.init_app(app)

with app.app_context():
    db.create_all()
```
