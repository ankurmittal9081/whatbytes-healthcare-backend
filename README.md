# Healthcare Backend API System

A robust, secure backend system for a healthcare application developed with **Django**, **Django REST Framework (DRF)**, **SimpleJWT**, and **PostgreSQL**.

> Developed for the WhatBytes Full Stack Developer Internship Technical Assignment.

---

## 🌟 Key Features

- **Authentication & Security**: Custom User model using email as unique identifier, bcrypt/PBKDF2 password hashing, and stateless JWT token authentication (`djangorestframework-simplejwt`).
- **Patient Management**: Full CRUD endpoints for patients, ensuring authenticated users can only view and manage patients they created.
- **Doctor Management**: Endpoints to register, retrieve, update, and manage medical professionals.
- **Patient-Doctor Mapping**: Assign doctors to patients with duplicate-assignment prevention via database unique constraints, query assigned doctors for any patient, and revoke assignments.
- **Environment Driven**: 100% configuration via environment variables (`python-dotenv`).
- **Testing**: 20 automated unit and integration tests covering all positive and negative test cases.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Django 5.x, Django REST Framework
- **Authentication**: `djangorestframework-simplejwt`
- **Database**: PostgreSQL (with SQLite fallback for local developer machines)
- **CORS Support**: `django-cors-headers`

---

## 📁 Project Architecture

```text
whatbytes-healthcare-backend/
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore patterns
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
├── postman_collection.json   # 1-Click Postman import collection
├── healthcare_backend/       # Core project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                 # Custom User & JWT Authentication app
├── patients/                 # Patient management app
├── doctors/                  # Doctor management app
└── mappings/                 # Patient-Doctor mapping app
```

---

## 🚀 Quickstart & Setup Guide

### 1. Clone & Setup Environment
```bash
# Clone the repository
git clone https://github.com/<your-username>/whatbytes-healthcare-backend.git
cd whatbytes-healthcare-backend

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Update `.env` with your PostgreSQL database credentials:
```ini
SECRET_KEY=your-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```
*(Note: If PostgreSQL is not installed locally, set `DB_ENGINE=django.db.backends.sqlite3` for zero-configuration SQLite).*

### 3. Run Migrations & Start Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Server will be live at `http://127.0.0.1:8000/`.

---

## 🧪 Running Automated Tests

Run the test suite covering all 20 test cases:
```bash
python manage.py test
```
**Output:**
```text
Ran 20 tests in 10.485s
OK
```

---

## 📚 API Documentation

### 1. Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Register a new user | No |
| `POST` | `/api/auth/login/` | Authenticate and obtain JWT access & refresh tokens | No |

#### `POST /api/auth/register/`
**Request Body:**
```json
{
  "name": "Ankur Mittal",
  "email": "ankur@example.com",
  "password": "SecurePassword123"
}
```
**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "Ankur Mittal",
    "email": "ankur@example.com",
    "created_at": "2026-10-18T20:25:00+05:30"
  },
  "tokens": {
    "refresh": "eyJhbGciOiJIUzI1NiIsIn...",
    "access": "eyJhbGciOiJIUzI1NiIsIn..."
  }
}
```

#### `POST /api/auth/login/`
**Request Body:**
```json
{
  "email": "ankur@example.com",
  "password": "SecurePassword123"
}
```
**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "name": "Ankur Mittal",
    "email": "ankur@example.com"
  },
  "tokens": {
    "refresh": "eyJhbGciOiJIUzI1NiIsIn...",
    "access": "eyJhbGciOiJIUzI1NiIsIn..."
  }
}
```

---

### 2. Patient Management Endpoints

> **Note:** Include header `Authorization: Bearer <access_token>` in all requests.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/patients/` | Add a new patient record (auto-bound to authenticated user) |
| `GET` | `/api/patients/` | Retrieve all patients created by the authenticated user |
| `GET` | `/api/patients/<id>/` | Get details of a specific patient |
| `PUT` | `/api/patients/<id>/` | Update patient details |
| `DELETE` | `/api/patients/<id>/` | Delete patient record |

#### `POST /api/patients/`
```json
{
  "name": "Ramesh Sharma",
  "age": 42,
  "gender": "Male",
  "contact_number": "9876543210",
  "address": "Mathura, UP",
  "medical_history": "Hypertension"
}
```

---

### 3. Doctor Management Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/doctors/` | Add a new doctor (Authenticated users only) |
| `GET` | `/api/doctors/` | Retrieve list of all doctors |
| `GET` | `/api/doctors/<id>/` | Get details of a specific doctor |
| `PUT` | `/api/doctors/<id>/` | Update doctor details |
| `DELETE` | `/api/doctors/<id>/` | Delete doctor record |

#### `POST /api/doctors/`
```json
{
  "name": "Dr. Priya Verma",
  "specialization": "Cardiologist",
  "email": "dr.priya@hospital.com",
  "phone_number": "9123456780",
  "years_of_experience": 10,
  "hospital_affiliation": "Metro Heart Institute"
}
```

---

### 4. Patient-Doctor Mapping Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/mappings/` | Assign a doctor to a patient |
| `GET` | `/api/mappings/` | Retrieve all patient-doctor mappings |
| `GET` | `/api/mappings/<patient_id>/` | Get all doctors assigned to a specific patient |
| `DELETE` | `/api/mappings/<id>/` | Remove a doctor from a patient (by mapping id) |

#### `POST /api/mappings/`
```json
{
  "patient": 1,
  "doctor": 1,
  "notes": "Weekly cardiac routine check"
}
```

#### `GET /api/mappings/1/`
**Response (200 OK):**
```json
{
  "patient_id": 1,
  "patient_name": "Ramesh Sharma",
  "total_doctors": 1,
  "doctors": [
    {
      "id": 1,
      "name": "Dr. Priya Verma",
      "specialization": "Cardiologist",
      "email": "dr.priya@hospital.com",
      "phone_number": "9123456780",
      "years_of_experience": 10,
      "hospital_affiliation": "Metro Heart Institute"
    }
  ]
}
```

---

## 📮 Testing with Postman
Import `postman_collection.json` into Postman:
1. Open Postman -> Click **Import**.
2. Select the `postman_collection.json` from the project root.
3. Call **Login User** or **Register User**; the access token is automatically saved into the environment collection variable `access_token`!
