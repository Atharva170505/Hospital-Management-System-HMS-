from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models to make them available
from models.user import User
from models.department import Department
from models.doctor import Doctor
from models.doctor_availability import DoctorAvailability
from models.patient import Patient
from models.appointment import Appointment
from models.treatment import Treatment

# Export all models
__all__ = [
    'db',
    'User',
    'Department',
    'Doctor',
    'DoctorAvailability',
    'Patient',
    'Appointment',
    'Treatment'
]
