# ⚡ OpenCliq | Employee Management & Attendance System

OpenCliq is a professional-grade HR management platform built with **Django**. It enables companies to track employee attendance, monitor team activity in real-time, and manage internal announcements through a modern, responsive dashboard.



## 🚀 Key Features

* **Real-time Attendance:** Interactive Check-in/Check-out system with automatic duration calculation.
* **Activity Visualization:** Weekly work-hour reports rendered using **Chart.js**.
* **Admin Management:** High-level overview of all employees, their current status (Online/Offline), and profile management.
* **Meeting Scheduler:** Admin-controlled announcement system to broadcast meetings and video links to the entire team.
* **Task Management:** AJAX-powered task list allowing employees to manage daily goals without page reloads.
* **Role-Based Security:** Distinct views and permissions for Staff (Managers) and Employees.

## 🛠️ Technical Stack

* **Backend:** Python / Django
* **Frontend:** Tailwind CSS, JavaScript (ES6+)
* **Database:** SQLite (Development) / PostgreSQL (Production ready)
* **Visualization:** Chart.js
* **Security:** Environment-based configuration (python-dotenv)

## 📦 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/OpenCliq-Attendance-System.git](https://github.com/YOUR_USERNAME/OpenCliq-Attendance-System.git)
    cd OpenCliq-Attendance-System
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup Environment Variables:**
    Create a `.env` file in the root directory:
    ```env
    SECRET_KEY=your_secret_key_here
    DEBUG=True
    ```

5.  **Run Migrations & Start Server:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## 📸 Screenshots
<img width="1918" height="862" alt="image" src="https://github.com/user-attachments/assets/a18e0035-94d8-4510-b02a-99894a07a684" />
<img width="1917" height="872" alt="image" src="https://github.com/user-attachments/assets/f0d4689f-8267-44dd-ba37-712dca9a4eda" />
<img width="1918" height="871" alt="image" src="https://github.com/user-attachments/assets/4ab520cb-3e10-4794-a945-1b25ded8d40e" />




## 🛡️ Future Roadmap
- [ ] Integration with Slack/Microsoft Teams notifications.
- [ ] Exportable PDF payroll reports.
- [ ] Geofencing for location-based check-ins.

---
Developed by **Ajay B V** – Feel free to reach out for collaboration!
