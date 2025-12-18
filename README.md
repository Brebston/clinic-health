# Clinic Health

Clinic Health is a learning Django project for a medical clinic.  
The project was created to practice Django fundamentals such as models, views, forms, authentication, and basic business logic.

### Demo:
- Login: Test
- Password: Qwerty123!
- URL: https://clinic-health-meip.onrender.com/

---

## Features

### Users
- User registration and login
- User profile page
- Store basic user information (full name, phone number, date of birth)

### Doctors
- Doctor profile
- Medical specialty
- Online / offline status
- View own appointments
- Update appointment status

### Appointments
- Create appointments with doctors
- Select available date and time
- Validation to prevent booking in the past
- Notes from patients
- Cancel appointments

### Admin Panel
- Manage users and doctors
- View and manage appointments
- Basic Django admin customization

---

## Tech Stack

- Python 3
- Django 5
- SQLite (default database)
- HTML / CSS
- JavaScript (basic usage)

---

## Project Structure

```
clinic-health/
├── accounts/        # user authentication and profiles
├── doctors/         # doctor profiles and specialties
├── appointments/   # appointment logic
├── core/            # main pages (home, about, etc.)
├── templates/
├── static/
└── manage.py
```

---

## Installation

1. Clone the repository
```bash
git clone <repository_url>
cd clinic-health
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Apply migrations
```bash
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Run development server
```bash
python manage.py runserver
```

Open in browser:
```
http://127.0.0.1:8000/
```

---

## Notes

- This project is not production ready
- It was created mainly for learning purposes
- Some parts of the logic and UI are simplified

---

## Author

Created as a learning Django project.
