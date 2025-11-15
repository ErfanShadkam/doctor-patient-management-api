# 📌 Doctor Patient Management API

A professional Django REST Framework project for managing doctors, patients, appointments, and prescriptions — built with JWT authentication, role-based permissions, and full Swagger documentation.

---

## 🚀 Features

### 🔐 Authentication
- JWT login / logout
- Register as **Doctor** or **Patient**
- Role-based permissions
- Secure password hashing

### 🧑‍⚕️ Doctor Module
- Doctor profile (specialty, bio, working hours)
- View assigned appointments
- Approve / cancel appointments
- Create prescriptions
- Filter appointments by status

### 👤 Patient Module
- Patient profile
- Book an appointment with doctors
- View or cancel own appointments
- View prescriptions

### 📅 Appointments
- Patient → Doctor booking system
- Status: Pending, Approved, Cancelled, Completed
- View appointments history

### 💊 Prescriptions
- Attach prescription to an appointment
- View prescriptions as patient

### 📘 Documentation
- Interactive API docs
- Built with **drf-spectacular**
- Visit: `/api/docs/`

---

## 🔑 Permissions

| Permission | Description |
|------------|-------------|
| `IsDoctor` | Only doctors can access specific actions |
| `IsPatient` | Only patients can access specific actions |
| `IsAppointmentOwnerOrDoctor` | Appointment can be accessed by the patient or the assigned doctor |
| `ReadOnlyForDoctors` | Doctors can only **view** (GET, LIST) doctor profiles |
| `IsDoctorOwnPatient` | Doctors can only access patients they have appointments with |

---

## 🗂 Models

### DoctorProfile

| Field | Type | Description |
|-------|------|-------------|
| `user` | OneToOneField | Linked to the Django User model |
| `full_name` | CharField | Doctor's full name |
| `specialization` | CharField | Doctor's specialty |
| `bio` | TextField | Doctor bio |
| `available_from` | TimeField | Start of available hours |
| `available_to` | TimeField | End of available hours |

### PatientProfile

| Field | Type | Description |
|-------|------|-------------|
| `user` | OneToOneField | Linked to the Django User model |
| `full_name` | CharField | Patient's full name |
| `birth_date` | DateField | Birth date |
| `medical_history` | TextField | Medical history |

### Appointment

| Field | Type | Description |
|-------|------|-------------|
| `doctor` | ForeignKey | Doctor assigned (nullable) |
| `patient` | ForeignKey | Patient creating the appointment |
| `scheduled_at` | DateTimeField | Date and time of appointment |
| `reason` | TextField | Reason for visit |
| `status` | CharField | `pending`, `confirmed`, `completed`, `cancelled` |
| `created_at` | DateTimeField | Auto-created timestamp |

### Prescription

| Field | Type | Description |
|-------|------|-------------|
| `appointment` | OneToOneField | Linked appointment |
| `notes` | TextField | Prescription notes |

---



## 🛠 Tech Stack
- **Backend:** Django 5, Django REST Framework
- **Authentication:** JWT (SimpleJWT)
- **API Docs:** drf-spectacular (Swagger)
- **Filtering:** django-filter
- **Database:** SQLite (default, can be switched to PostgreSQL)
- **Environment:** Python 3.11+

---

## 📂 Project Structure

![Swagger UI](screenshots/swagger.png)

[Swagger UI PDF](screenshots/api_docs.pdf)

---

## 💻 Installation

1. **Clone the repository**
```bash
git clone https://github.com/ErfanShadkam/doctor-patient-management-api.git
cd doctor-patient-management-api
```
2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. **Install dependencies**
```
pip install -r requirements.txt
```

4. **Apply migrations**
```
python manage.py migrate
```

5. **Create superuser (optional)**
```
python manage.py createsuperuser
```

6. **Run the server**
```
python manage.py runserver
```
7. **Access API Documentation**

Visit http://127.0.0.1:8000/api/docs/