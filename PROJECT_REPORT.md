# Project Report Template

## Student Details
- **Name:** [Your Name]
- **Roll Number:** [Your Roll Number]
- **Email:** [Your Email]

## Project Details

### Problem Statement
The project involves building a Hospital Management System (HMS) to help hospitals efficiently manage patients, doctors, appointments, and treatments. The system addresses the challenges of manual record-keeping and disconnected software by providing a centralized web application.

### Approach
1. **Database Design:** Created a normalized database schema with 7 tables (users, departments, doctors, doctor_availability, patients, appointments, treatments)
2. **Backend Development:** Used Flask framework with SQLAlchemy ORM for database operations
3. **Authentication:** Implemented Flask-Login for secure user authentication and role-based access control
4. **Frontend Development:** Used Bootstrap 5 with Jinja2 templates for responsive design
5. **Features Implementation:** Systematically implemented all core features for Admin, Doctor, and Patient roles
6. **API Development:** Created REST API endpoints for external integrations

## AI/LLM Declaration

### Extent of AI/LLM Usage
[Please fill in your usage - Example below]

**Example:**
- Used GitHub Copilot for code completion and suggestions: 30%
- Used ChatGPT for debugging specific errors: 10%
- All core logic and architecture designed independently: 60%
- OR: No AI/LLM tools were used

[Describe specifically what you used AI for and what you did yourself]

## Frameworks and Libraries Used

### Backend
- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy 3.1.1** - ORM for database operations
- **Flask-Login 0.6.3** - User session management
- **Werkzeug 3.0.1** - Password hashing and security

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **Bootstrap 5.3** - Responsive design framework
- **Bootstrap Icons** - Icon library
- **Jinja2** - Template engine (included with Flask)

### Database
- **SQLite** - Lightweight relational database

## ER Diagram

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│    Users    │         │  Departments │         │   Doctors   │
├─────────────┤         ├──────────────┤         ├─────────────┤
│ id (PK)     │         │ id (PK)      │         │ id (PK)     │
│ email       │         │ name         │    ┌────│ user_id(FK) │
│ password    │         │ description  │    │    │ dept_id(FK) │───┐
│ role        │         │ created_at   │    │    │ name        │   │
│ is_active   │         └──────────────┘    │    │ phone       │   │
│ created_at  │                │            │    │ qualification│  │
└─────────────┘                │            │    │ experience  │   │
       │                       │            │    │ consult_fee │   │
       │                       └────────────┼────│ created_at  │   │
       │                                    │    └─────────────┘   │
       │                                    │            │         │
       │                                    │            │         │
       ├────────────────────────────────────┤            │         │
       │                                                 │         │
       ▼                                                 │         │
┌─────────────┐                                         │         │
│  Patients   │                                         │         │
├─────────────┤                                         │         │
│ id (PK)     │                                         │         │
│ user_id(FK) │───┐                                     │         │
│ name        │   │                                     │         │
│ phone       │   │                                     │         │
│ dob         │   │                                     │         │
│ gender      │   │     ┌──────────────────┐            │         │
│ address     │   │     │  Appointments    │            │         │
│ emergency   │   │     ├──────────────────┤            │         │
│ blood_group │   └────▶│ id (PK)          │◀───────────┘         │
│ created_at  │         │ patient_id (FK)  │                      │
└─────────────┘         │ doctor_id (FK)   │                      │
                        │ appt_date        │                      │
                        │ appt_time        │                      │
                        │ status           │                      │
                        │ reason           │                      │
                        │ created_at       │                      │
                        │ updated_at       │                      │
                        └──────────────────┘                      │
                                │                                 │
                                │                                 │
                                ▼                                 │
                        ┌──────────────────┐                      │
                        │   Treatments     │                      │
                        ├──────────────────┤                      │
                        │ id (PK)          │                      │
                        │ appt_id (FK)     │                      │
                        │ diagnosis        │                      │
                        │ prescription     │                      │
                        │ notes            │                      │
                        │ follow_up_date   │                      │
                        │ created_at       │                      │
                        │ updated_at       │                      │
                        └──────────────────┘                      │
                                                                  │
                        ┌──────────────────────┐                  │
                        │ Doctor_Availability  │                  │
                        ├──────────────────────┤                  │
                        │ id (PK)              │                  │
                        │ doctor_id (FK)       │◀─────────────────┘
                        │ date                 │
                        │ start_time           │
                        │ end_time             │
                        │ is_available         │
                        │ created_at           │
                        └──────────────────────┘

Relationships:
- Users 1:1 Doctor (one user can be one doctor)
- Users 1:1 Patient (one user can be one patient)
- Departments 1:N Doctors (one department has many doctors)
- Doctors 1:N Appointments (one doctor has many appointments)
- Patients 1:N Appointments (one patient has many appointments)
- Appointments 1:1 Treatment (one appointment has one treatment record)
- Doctors 1:N Doctor_Availability (one doctor has many availability slots)
```

## API Resource Endpoints

### 1. GET /api/departments
**Description:** Get all departments with doctor count  
**Authentication:** Not required  
**Response:** JSON array of department objects

### 2. GET /api/doctors
**Description:** Get all doctors (optional filter by department)  
**Parameters:** `department_id` (optional)  
**Authentication:** Not required  
**Response:** JSON array of doctor objects

### 3. GET /api/appointments/<appointment_id>
**Description:** Get specific appointment details  
**Authentication:** Required (logged in user)  
**Response:** JSON object with appointment details

### 4. GET /api/doctor/<doctor_id>/availability
**Description:** Get doctor's availability for next 7 days  
**Authentication:** Not required  
**Response:** JSON array of availability slots

## Video Presentation

**Drive Link:** [Insert your Google Drive link here with "Anyone with the link" access]

**Video Duration:** [X minutes]

**Video Content:**
- Introduction and overview
- Problem statement approach
- Key features demonstration
- Additional features implemented
- Live demo walkthrough

## Additional Features Implemented

1. **REST API Endpoints** - Created 4 API resources for external integration
2. **Doctor Availability Management** - 7-day scheduling system
3. **Search Functionality** - Search doctors and patients by multiple criteria
4. **Responsive Design** - Mobile-friendly Bootstrap interface
5. **Password Security** - Secure password hashing with pbkdf2:sha256
6. **Role-based Access Control** - Decorator-based route protection
7. **Flash Messages** - User-friendly feedback system
8. **Form Validation** - Both frontend (HTML5) and backend validation

## Conclusion

The Hospital Management System successfully implements all core requirements and additional features. The system provides a secure, efficient, and user-friendly platform for managing hospital operations. The use of Flask, SQLAlchemy, and Bootstrap ensures scalability and maintainability.

---

**Date of Submission:** [Insert Date]  
**Declaration:** I hereby declare that this project is my original work and all sources of assistance have been properly acknowledged.

**Signature:** _________________
