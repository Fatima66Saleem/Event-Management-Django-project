# 📅 Event Management System (EMS) - Django Web Application

**Event Management System** is a full-featured web platform built using the **Django** framework. It allows users to organize, manage, and track various events through a centralized dashboard. This project focuses on high performance, secure authentication, and a user-friendly interface.

---

## 🚀 Project Overview
The main goal of this project is to automate the manual process of event planning. It provides a structured way to store event details, manage organizers, and ensure all data is synchronized with a backend database.

### ✨ Key Features & Functionalities
| Feature | Description |
| :--- | :--- |
| **User Authentication** | Secure Login, Logout, and User Registration system. |
| **Event Dashboard** | A centralized view of all active and upcoming events. |
| **Full CRUD Support** | Ability to **Create, Read, Update, and Delete** events. |
| **Database Integration** | Uses SQLite3 to store event titles, dates, and descriptions. |
| **Search & Filter** | Easily find specific events from the management list. |
| **Responsive UI** | Designed to work perfectly on Mobile, Tablet, and Desktop. |

---

## 🛠️ Technical Stack (Tools Used)
* **Backend Framework:** Django 5.0 (Python Based)
* **Frontend Technologies:** HTML5, CSS3 (Custom Styling), JavaScript
* **Database:** SQLite (Relational Database Management)
* **Environment:** Localhost Development Server

---

## 📂 Project Structure & Navigation
To understand how the project is organized, here is a quick look at the core files:
* `event_management/`: The main project configuration folder (settings, urls).
* `events/`: The primary app containing the logic (views, models, templates).
* `templates/`: Contains the HTML files for the Frontend.
* `manage.py`: The command-line utility for administrative tasks.
* `db.sqlite3`: The local database file containing all event records.

---

## ⚙️ How to Setup & Run Locally
1.  **Download the Project:** Click the **Code** button and select **Download ZIP**.
2.  **Extract Files:** Unzip the folder on your computer.
3.  **Open Terminal:** Open CMD or Terminal in the project root directory.
4.  **Install Django:** (If not already installed)
    ```bash
    pip install django
    ```
5.  **Initialize Database:**
    ```bash
    python manage.py migrate
    ```
6.  **Create Admin (Optional):** To access the Django Admin Panel:
    ```bash
    python manage.py createsuperuser
    ```
7.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```
8.  **Launch Website:** Open `http://127.0.0.1:8000/` in your browser.

---

## 👩‍🎓 Academic Profile
* **Project Title:** Event Management System
* **Developer:** Fatima Saleem
* **Institute:** Riphah International University Sahiwal
* **Semester:** Final Semester Project

---

> **Note:** This project is part of my academic portfolio. For any queries regarding the setup or code logic, feel free to reach out.
