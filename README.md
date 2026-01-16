# Smart Expense Tracker

A full-stack web application to track personal expenses with user authentication, analytics, and a clean dashboard.

## 🚀 Features
- User registration and login (Flask-Login)
- Secure password hashing
- Add and manage expenses
- User-specific expense data
- Category-wise expense analytics (Pie Chart)
- Delete all expenses option
- Responsive UI using Bootstrap

## 🛠 Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite, SQLAlchemy
- **Authentication:** Flask-Login, Werkzeug
- **Frontend:** HTML, Bootstrap
- **Charts:** Chart.js
- **Version Control:** Git & GitHub

## 📂 Project Structure
Smart-Expense-Tracker/
│── app.py
│── requirements.txt
│── README.md
│── templates/
│ ├── login.html
│ ├── register.html
│ └── dashboard.html
## ⚙️ How to Run Locally

```bash
git clone https://github.com/Souharda/Smart-Expense-Tracker.git
cd Smart-Expense-Tracker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
Open browser:

http://127.0.0.1:5000
