# AI-Powered Employee Recruitment System

## 📌 Project Overview

The AI-Powered Employee Recruitment System is a web-based application developed using Python and Django. The system automates the recruitment process by allowing candidates to register, upload resumes, and automatically extract skills from uploaded resumes. HR personnel can post job openings, and the system calculates candidate-job matching scores using AI-based skill comparison.

---

## 🚀 Features

### Candidate Module

* Candidate Registration
* Candidate Login
* Candidate Dashboard
* Resume Upload (PDF)

### HR Module

* Post New Job Openings
* Manage Job Requirements
* View Candidate Data

### AI Features

* Resume Parsing
* Automatic Skill Extraction
* Candidate-Job Match Score Calculation
* Resume Skill Analysis

### Admin Module

* Manage Candidates
* Manage Resumes
* Manage Jobs
* Django Admin Dashboard

---

## 🛠 Technologies Used

### Frontend

* HTML
* CSS
* Bootstrap 5

### Backend

* Python
* Django

### Database

* SQLite

### AI / NLP

* PDFPlumber
* Python Skill Matching Algorithm

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

AI_RECRUITMENT_SYSTEM

├── accounts

├── recruitment_system

├── templates

├── media

├── manage.py

├── db.sqlite3

└── README.md

---

## ⚙️ Installation Steps

### Clone Repository

```bash
git clone https://github.com/Jagadeesh730/AI-Recruitment-System.git
```

### Move into Project

```bash
cd AI-Recruitment-System
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install django
pip install pdfplumber
```

### Run Migrations

```bash
python manage.py migrate
```

### Start Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 🎯 AI Matching Workflow

1. Candidate uploads resume.
2. System extracts text from PDF.
3. Skills are identified automatically.
4. HR posts job requirements.
5. System compares candidate skills with required skills.
6. Match score is generated.
7. Candidates can be ranked based on score.

---

## 📈 Future Enhancements

* Dynamic Candidate Ranking
* Interview Scheduling
* Email Notifications
* Resume Recommendation System
* Machine Learning Based Candidate Selection
* Cloud Deployment (AWS/Render)

---

## 👨‍💻 Author

**Jagadeesh C**

GitHub: https://github.com/Jagadeesh730

---

## ⭐ Project Status

Completed Core Modules:

* Registration
* Login
* Resume Upload
* Skill Extraction
* Job Posting
* Match Score Calculation

Future Versions:

* Candidate Ranking
* Interview Management
* Advanced AI Recommendations
