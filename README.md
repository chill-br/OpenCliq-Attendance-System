# OpenCliq | Attendance & Team Management

OpenCliq is a modern, high-performance **Django** application designed to streamline workplace attendance, team communication, and productivity. It features a sleek, emerald-themed dashboard with real-time tracking.

---

## 🚀 Key Features

### 🕒 Smart Attendance System
*   **Mode Selection:** Toggle between `Office` and `Remote` work modes.
*   **Geolocation:** Office check-ins require GPS verification (via Geolocation API).
*   **Live Timer:** A real-time duration counter that tracks your shift to the second.
*   **Break Management:** Easy "Start/End Break" buttons for lunch and short intervals.

### 📢 Team Interaction
*   **Team Blog:** An internal social feed where members can post text updates and images.
*   **Live Status:** An "Online Now" sidebar showing currently checked-in team members with status indicators.

### ✅ Productivity & Scheduling
*   **Focus List:** A built-in To-Do list to manage daily tasks without leaving the dashboard.
*   **Meeting Hub:** A dedicated section for scheduled meetings with direct "Join Call" links.
*   **History Logs:** Detailed table view of past attendance with CSV export capability.

### 📊 Analytics
*   **Visual Reports:** Activity trends visualized via **Chart.js**.
*   **Quick Stats:** Instant view of total hours today, monthly totals, and average check-in times.

---

## 🛠️ Tech Stack

*   **Backend:** Python / Django 5.x
*   **Frontend:** Tailwind CSS (Styling), JavaScript (AJAX/Real-time logic)
*   **Database:** SQLite / PostgreSQL
*   **APIs:** Browser Geolocation API
*   **Libraries:** Chart.js, FontAwesome 6

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/chill-br/OpenCliq-Attendance-System.git](https://github.com/chill-br/OpenCliq-Attendance-System.git)
   cd OpenCliq-Attendance-System
2. Create and activate Virtual Environment:

Bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

3. **Install Dependencies:**

Bash
pip install django pillow

4. **Run Migrations:**

Bash
* python manage.py makemigrations
* python manage.py migrate


5. **Start the Server:**
   ```bash
   python manage.py runserver
