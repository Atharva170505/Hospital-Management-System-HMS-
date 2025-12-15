from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, date
from functools import wraps
from models import db, User, Doctor, Patient, Appointment, Treatment, Department, DoctorAvailability

app = Flask(__name__)
app.config['SECRET_KEY'] = 'just_a_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please login to access this page.', 'warning')
                return redirect(url_for('login'))
            if current_user.role != role:
                flash('You do not have permission to access this page.', 'go back')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def init_db():
    with app.app_context():
        db.create_all()
        
        if Department.query.count() == 0:
            departments = [
                Department(name='Cardiology', description='Heart and cardiovascular system'),
                Department(name='Neurology', description='Brain and nervous system'),
                Department(name='Orthopedics', description='Bones, joints, and muscles'),
                Department(name='Pediatrics', description='Children health'),
                Department(name='Dermatology', description='Skin, hair, and nails'),
                Department(name='General Medicine', description='General health consultation'),
            ]
            for dept in departments:
                db.session.add(dept)
            db.session.commit()
            print("Default departments created.")
        
        admin = User.query.filter_by(email='admin@hospital.com').first()
        if not admin:
            admin = User(
                email='admin@hospital.com',
                password=generate_password_hash('admin123', method='pbkdf2:sha256'),
                role='admin',
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created. Email: admin@hospital.com, Password: admin123")

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif current_user.role == 'patient':
            return redirect(url_for('patient_dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact admin.', 'danger')
                return redirect(url_for('login'))
            
            login_user(user)
            flash('Login successful!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            elif user.role == 'patient':
                return redirect(url_for('patient_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        address = request.form.get('address')
        emergency_contact = request.form.get('emergency_contact')
        blood_group = request.form.get('blood_group')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('login'))
        
        user = User(
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            role='patient',
            is_active=True
        )
        db.session.add(user)
        db.session.flush()
        
        patient = Patient(
            user_id=user.id,
            name=name,
            phone=phone,
            date_of_birth=datetime.strptime(dob, '%Y-%m-%d').date() if dob else None,
            gender=gender,
            address=address,
            emergency_contact=emergency_contact,
            blood_group=blood_group
        )
        db.session.add(patient)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    pending_appointments = Appointment.query.filter_by(status='Booked').count()
    
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_doctors=total_doctors,
                         total_patients=total_patients,
                         total_appointments=total_appointments,
                         pending_appointments=pending_appointments,
                         recent_appointments=recent_appointments)

@app.route('/admin/doctors')
@login_required
@role_required('admin')
def admin_doctors():
    search_query = request.args.get('search', '')
    
    if search_query:
        doctors = Doctor.query.filter(
            db.or_(
                Doctor.name.ilike(f'%{search_query}%'),
                Department.name.ilike(f'%{search_query}%')
            )
        ).join(Department).all()
    else:
        doctors = Doctor.query.all()
    
    return render_template('admin/doctors.html', doctors=doctors, search_query=search_query)

@app.route('/admin/doctor/add', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_add_doctor():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        department_id = request.form.get('department_id')
        qualification = request.form.get('qualification')
        experience_years = request.form.get('experience_years')
        consultation_fee = request.form.get('consultation_fee')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('admin_add_doctor'))
        
        user = User(
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            role='doctor',
            is_active=True
        )
        db.session.add(user)
        db.session.flush()
        
        doctor = Doctor(
            user_id=user.id,
            name=name,
            phone=phone,
            department_id=department_id,
            qualification=qualification,
            experience_years=int(experience_years) if experience_years else 0,
            consultation_fee=float(consultation_fee) if consultation_fee else 0
        )
        db.session.add(doctor)
        db.session.commit()
        
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('admin_doctors'))
    
    departments = Department.query.all()
    return render_template('admin/add_doctor.html', departments=departments)

@app.route('/admin/doctor/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    
    if request.method == 'POST':
        doctor.name = request.form.get('name')
        doctor.phone = request.form.get('phone')
        doctor.department_id = request.form.get('department_id')
        doctor.qualification = request.form.get('qualification')
        doctor.experience_years = int(request.form.get('experience_years', 0))
        doctor.consultation_fee = float(request.form.get('consultation_fee', 0))
        
        db.session.commit()
        flash('Doctor updated successfully!', 'success')
        return redirect(url_for('admin_doctors'))
    
    departments = Department.query.all()
    return render_template('admin/edit_doctor.html', doctor=doctor, departments=departments)

@app.route('/admin/doctor/delete/<int:doctor_id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    user = doctor.user
    
    appointment_count = len(doctor.appointments)
    if appointment_count > 0:
        flash(f'Cannot delete doctor. They have {appointment_count} appointment(s) associated. Please reassign or delete appointments first.', 'danger')
        return redirect(url_for('admin_doctors'))
    
    db.session.delete(doctor)
    db.session.delete(user)
    db.session.commit()
    
    flash('Doctor deleted successfully!', 'success')
    return redirect(url_for('admin_doctors'))

@app.route('/admin/patients')
@login_required
@role_required('admin')
def admin_patients():
    search_query = request.args.get('search', '')
    
    if search_query:
        patients = Patient.query.filter(
            db.or_(
                Patient.name.ilike(f'%{search_query}%'),
                Patient.phone.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        patients = Patient.query.all()
    
    return render_template('admin/patients.html', patients=patients, search_query=search_query)

@app.route('/admin/patient/edit/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    if request.method == 'POST':
        patient.name = request.form.get('name')
        patient.phone = request.form.get('phone')
        patient.gender = request.form.get('gender')
        patient.address = request.form.get('address')
        patient.emergency_contact = request.form.get('emergency_contact')
        patient.blood_group = request.form.get('blood_group')
        
        dob = request.form.get('dob')
        if dob:
            patient.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('admin_patients'))
    
    return render_template('admin/edit_patient.html', patient=patient)

@app.route('/admin/patient/delete/<int:patient_id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    user = patient.user
    
    appointment_count = len(patient.appointments)
    if appointment_count > 0:
        flash(f'Cannot delete patient. They have {appointment_count} appointment(s) associated. Please cancel or complete appointments first.', 'danger')
        return redirect(url_for('admin_patients'))
    
    db.session.delete(patient)
    db.session.delete(user)
    db.session.commit()
    
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('admin_patients'))

@app.route('/admin/appointments')
@login_required
@role_required('admin')
def admin_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('admin/appointments.html', appointments=appointments)

@app.route('/doctor/dashboard')
@login_required
@role_required('doctor')
def doctor_dashboard():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    today = date.today()
    week_end = today + timedelta(days=7)
    
    upcoming_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date >= today,
        Appointment.appointment_date <= week_end,
        Appointment.status == 'Booked'
    ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
    
    today_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date == today
    ).all()
    
    patients = Patient.query.join(Appointment).filter(Appointment.doctor_id == doctor.id).distinct().all()
    
    return render_template('doctor/dashboard.html',
                         doctor=doctor,
                         upcoming_appointments=upcoming_appointments,
                         today_appointments=today_appointments,
                         patients=patients)

@app.route('/doctor/appointments')
@login_required
@role_required('doctor')
def doctor_appointments():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('doctor/appointments.html', appointments=appointments)

@app.route('/doctor/appointment/<int:appointment_id>/complete', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def doctor_complete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    if appointment.doctor_id != doctor.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('doctor_appointments'))
    
    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis')
        prescription = request.form.get('prescription')
        notes = request.form.get('notes')
        follow_up = request.form.get('follow_up_date')
        
        appointment.status = 'Completed'
        
        treatment = Treatment(
            appointment_id=appointment.id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes,
            follow_up_date=datetime.strptime(follow_up, '%Y-%m-%d').date() if follow_up else None
        )
        db.session.add(treatment)
        db.session.commit()
        
        flash('Appointment completed and treatment recorded!', 'success')
        return redirect(url_for('doctor_appointments'))
    
    return render_template('doctor/complete_appointment.html', appointment=appointment)

@app.route('/doctor/patient/<int:patient_id>/history')
@login_required
@role_required('doctor')
def doctor_patient_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    appointments = Appointment.query.filter_by(
        patient_id=patient_id,
        doctor_id=doctor.id,
        status='Completed'
    ).order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('doctor/patient_history.html', patient=patient, appointments=appointments)

@app.route('/doctor/availability', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def doctor_availability():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        today = date.today()
        week_end = today + timedelta(days=7)
        DoctorAvailability.query.filter(
            DoctorAvailability.doctor_id == doctor.id,
            DoctorAvailability.date >= today,
            DoctorAvailability.date <= week_end
        ).delete()
        
        for i in range(7):
            date_key = (today + timedelta(days=i)).strftime('%Y-%m-%d')
            is_available = request.form.get(f'available_{date_key}')
            
            if is_available:
                start_time = request.form.get(f'start_time_{date_key}')
                end_time = request.form.get(f'end_time_{date_key}')
                
                availability = DoctorAvailability(
                    doctor_id=doctor.id,
                    date=(today + timedelta(days=i)),
                    start_time=start_time,
                    end_time=end_time,
                    is_available=True
                )
                db.session.add(availability)
        
        db.session.commit()
        flash('Availability updated successfully!', 'success')
        return redirect(url_for('doctor_dashboard'))
    
    today = date.today()
    availability_dict = {}
    dates_list = []
    for i in range(7):
        current_date = today + timedelta(days=i)
        avail = DoctorAvailability.query.filter_by(
            doctor_id=doctor.id,
            date=current_date
        ).first()
        date_str = current_date.strftime('%Y-%m-%d')
        availability_dict[date_str] = avail
        dates_list.append({
            'date': current_date,
            'date_str': date_str,
            'day_name': current_date.strftime('%A, %B %d, %Y')
        })
    
    return render_template('doctor/availability.html', availability=availability_dict, dates=dates_list)

@app.route('/patient/dashboard')
@login_required
@role_required('patient')
def patient_dashboard():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    departments = Department.query.all()
    
    today = date.today()
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date >= today,
        Appointment.status == 'Booked'
    ).order_by(Appointment.appointment_date).all()
    
    week_end = today + timedelta(days=7)
    available_doctors = Doctor.query.join(DoctorAvailability).filter(
        DoctorAvailability.date >= today,
        DoctorAvailability.date <= week_end,
        DoctorAvailability.is_available == True
    ).distinct().all()
    
    return render_template('patient/dashboard.html',
                         patient=patient,
                         departments=departments,
                         upcoming_appointments=upcoming_appointments,
                         available_doctors=available_doctors)

@app.route('/patient/profile', methods=['GET', 'POST'])
@login_required
@role_required('patient')
def patient_profile():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        patient.name = request.form.get('name')
        patient.phone = request.form.get('phone')
        patient.gender = request.form.get('gender')
        patient.address = request.form.get('address')
        patient.emergency_contact = request.form.get('emergency_contact')
        patient.blood_group = request.form.get('blood_group')
        
        dob = request.form.get('dob')
        if dob:
            patient.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('patient_dashboard'))
    
    return render_template('patient/profile.html', patient=patient)

@app.route('/patient/doctors')
@login_required
@role_required('patient')
def patient_doctors():
    search_query = request.args.get('search', '')
    department_id = request.args.get('department')
    
    query = Doctor.query.join(Department)
    
    if search_query:
        query = query.filter(
            db.or_(
                Doctor.name.ilike(f'%{search_query}%'),
                Department.name.ilike(f'%{search_query}%')
            )
        )
    
    if department_id:
        query = query.filter(Doctor.department_id == department_id)
    
    doctors = query.all()
    departments = Department.query.all()
    
    return render_template('patient/doctors.html',
                         doctors=doctors,
                         departments=departments,
                         search_query=search_query,
                         selected_department=department_id)

@app.route('/patient/book-appointment/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@role_required('patient')
def patient_book_appointment(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        reason = request.form.get('reason')
        
        existing = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=datetime.strptime(appointment_date, '%Y-%m-%d').date(),
            appointment_time=appointment_time
        ).first()
        
        if existing:
            flash('This time slot is already booked. Please choose another time.', 'danger')
            return redirect(url_for('patient_book_appointment', doctor_id=doctor_id))
        
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            appointment_date=datetime.strptime(appointment_date, '%Y-%m-%d').date(),
            appointment_time=appointment_time,
            reason=reason,
            status='Booked'
        )
        db.session.add(appointment)
        db.session.commit()
        
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient_appointments'))
    
    today = date.today()
    availability = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor_id,
        DoctorAvailability.date >= today,
        DoctorAvailability.date <= today + timedelta(days=7),
        DoctorAvailability.is_available == True
    ).all()
    
    return render_template('patient/book_appointment.html', doctor=doctor, availability=availability)

@app.route('/patient/appointments')
@login_required
@role_required('patient')
def patient_appointments():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('patient/appointments.html', appointments=appointments)

@app.route('/patient/appointment/<int:appointment_id>/cancel', methods=['POST'])
@login_required
@role_required('patient')
def patient_cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    if appointment.patient_id != patient.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('patient_appointments'))
    
    if appointment.status != 'Booked':
        flash('Only booked appointments can be cancelled.', 'warning')
        return redirect(url_for('patient_appointments'))
    
    appointment.status = 'Cancelled'
    db.session.commit()
    
    flash('Appointment cancelled successfully!', 'success')
    return redirect(url_for('patient_appointments'))

@app.route('/patient/history')
@login_required
@role_required('patient')
def patient_history():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    completed_appointments = Appointment.query.filter_by(
        patient_id=patient.id,
        status='Completed'
    ).order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('patient/history.html', appointments=completed_appointments)

@app.route('/api/departments', methods=['GET'])
def api_get_departments():
    departments = Department.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'description': d.description,
        'doctor_count': len(d.doctors)
    } for d in departments])

@app.route('/api/doctors', methods=['GET'])
def api_get_doctors():
    department_id = request.args.get('department_id')
    
    query = Doctor.query
    if department_id:
        query = query.filter_by(department_id=department_id)
    
    doctors = query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'department': d.department.name,
        'qualification': d.qualification,
        'experience_years': d.experience_years,
        'consultation_fee': d.consultation_fee
    } for d in doctors])

@app.route('/api/doctor/<int:doctor_id>/availability', methods=['GET'])
def api_doctor_availability(doctor_id):
    today = date.today()
    availability = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor_id,
        DoctorAvailability.date >= today,
        DoctorAvailability.date <= today + timedelta(days=7),
        DoctorAvailability.is_available == True
    ).all()
    
    return jsonify([{
        'date': a.date.strftime('%Y-%m-%d'),
        'start_time': a.start_time,
        'end_time': a.end_time
    } for a in availability])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
