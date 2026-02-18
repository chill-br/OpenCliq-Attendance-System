
# 🏢 OpenCliq Attendance System

A modern, Django-powered attendance and team management system. This application allows administrators to manage employee attendance, schedule meetings, and post team announcements through a clean, responsive dashboard.

## ✨ Features
* **Smart Dashboard**: Real-time overview of attendance and upcoming events.
* **Meeting Scheduler**: Easy interface for admins to post video call links and agendas.
* **Announcements**: Post team-wide updates with instant visibility.
* **Secure Authentication**: Role-based access control (Staff vs. Employee).
* **Responsive UI**: Built with Tailwind CSS for a seamless experience on mobile and desktop.

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.12+
* Git

### 2. Installation
Clone the repository to your local machine:
```bash
git clone [https://github.com/chill-br/OpenCliq-Attendance-System.git](https://github.com/chill-br/OpenCliq-Attendance-System.git)
cd OpenCliq-Attendance-System

```

### 3. Setup Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
.\venv\Scripts\activate

# Activate venv (Mac/Linux)
source venv/bin/activate

```

### 4. Install Dependencies

```bash
pip install -r requirements.txt

```

### 5. Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate

```

### 6. Create Admin User

```bash
python manage.py createsuperuser

```

### 7. Run the Server

```bash
python manage.py runserver

```

Visit `http://127.0.0.1:8000` to see the app!

---

## 🛠️ Tech Stack

* **Backend**: Django (Python)
* **Frontend**: Tailwind CSS, FontAwesome
* **Database**: SQLite (Development)
* **State Management**: JavaScript (Fetch API)

---

## 📸 Screenshots

<img width="1918" height="882" alt="image" src="https://github.com/user-attachments/assets/27a53b25-756c-43ba-8d43-15fe51341f31" />

<img width="1918" height="893" alt="image" src="https://github.com/user-attachments/assets/a8b5edd5-ca42-4739-8433-2bd74e3549c6" />


---

## 📄 License

This project is for educational purposes.

```
