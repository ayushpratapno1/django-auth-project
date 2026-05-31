# Django Authentication System

A production-ready authentication system built with Django, PostgreSQL, Google OAuth, and Render deployment.

## Project Overview

This project was created to learn and implement a complete authentication system before integrating similar functionality into larger AI/ML projects such as a Movie Recommendation System.

The project demonstrates:

* User Registration
* User Login
* User Logout
* Google OAuth Authentication
* User Profile Management
* Admin Dashboard
* PostgreSQL Database Integration
* Production Deployment on Render
* Environment Variable Management

The application is fully deployed and supports authentication from any device through the internet.

---

# Live Features

### Authentication

* User Signup
* User Login
* User Logout
* Google Sign-In using OAuth 2.0
* Session Management

### User Profile

* View Profile
* Edit Profile
* Upload Profile Picture
* Update Bio
* Add GitHub Profile
* Add LinkedIn Profile

### Dashboard

* View Total Users
* View Active Users
* View Staff Users
* View User Details
* View Registration Statistics

### Admin Management

* Django Admin Panel
* User Management
* Profile Management
* Google OAuth Management

---

# Tech Stack

## Backend

* Django 6
* Django ORM
* Django Allauth

## Frontend

* HTML
* CSS
* Django Templates

## Database

* SQLite (Development)
* PostgreSQL (Production)

## Authentication

* Django Authentication System
* Google OAuth 2.0
* Django Allauth

## Deployment

* Render
* Gunicorn
* WhiteNoise

## Environment Management

* Python Dotenv
* Environment Variables

---

# Project Architecture

```text
User
 │
 ▼
Browser
 │
 ▼
Django Views
 │
 ▼
Authentication Layer
 │
 ├── Manual Login
 │
 ├── Manual Signup
 │
 └── Google OAuth Login
 │
 ▼
Django ORM
 │
 ▼
PostgreSQL Database
 │
 ▼
User Data
Profiles
Sessions
Google Accounts
```

---

# Project Structure

```text
django-auth-project/

│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── signals.py
│   └── templates/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── profile.html
│   ├── edit_profile.html
│   └── dashboard.html
│
├── media/
├── static/
├── requirements.txt
├── build.sh
├── manage.py
└── README.md
```

---

# Database Design

## User Model

Uses Django's built-in User model.

```text
User
 ├── username
 ├── first_name
 ├── last_name
 ├── email
 ├── password
 ├── is_staff
 ├── is_active
 └── date_joined
```

---

## Profile Model

Each user has exactly one profile.

```text
Profile
 ├── user (One-To-One Field)
 ├── bio
 ├── github
 ├── linkedin
 └── profile_picture
```

Relationship:

```text
User
  │
  └── One-To-One
           │
           ▼
        Profile
```

---

# Authentication Flow

## Manual Signup

```text
User
 │
 ▼
Signup Form
 │
 ▼
Create User
 │
 ▼
Create Profile
 │
 ▼
Store in Database
 │
 ▼
Login
```

---

## Manual Login

```text
User
 │
 ▼
Login Form
 │
 ▼
Authenticate User
 │
 ▼
Create Session
 │
 ▼
Redirect Home
```

---

## Google Login

```text
User
 │
 ▼
Continue with Google
 │
 ▼
Google OAuth
 │
 ▼
User Grants Permission
 │
 ▼
Google Returns User Data
 │
 ▼
Django Allauth
 │
 ▼
Create User
 │
 ▼
Create Profile
 │
 ▼
Login User
```

---

# Profile Creation Automation

The project uses Django Signals.

Whenever a new user is created:

```text
User Created
 │
 ▼
Signal Triggered
 │
 ▼
Profile Created Automatically
```

This ensures every user always has a profile.

---

# Admin Dashboard

Custom dashboard includes:

```text
Total Users

Total Profiles

Active Users

Inactive Users

Staff Users

Registered Users Table
```

Displayed information:

```text
Username

Full Name

Email

Date Joined

Staff Status

Active Status
```

---

# Environment Variables

Sensitive information is stored using environment variables.

Example:

```env
SECRET_KEY=

DEBUG=

ALLOWED_HOSTS=

DATABASE_URL=

SUPERUSER_USERNAME=

SUPERUSER_EMAIL=

SUPERUSER_PASSWORD=
```

Google OAuth:

```env
GOOGLE_CLIENT_ID=

GOOGLE_CLIENT_SECRET=
```

---

# Local Development

Create virtual environment:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Run server:

```bash
python manage.py runserver
```

---

# Production Deployment

Hosted on Render.

Deployment workflow:

```text
GitHub
 │
 ▼
Render
 │
 ▼
Build Script
 │
 ├── Install Requirements
 ├── Collect Static Files
 ├── Run Migrations
 └── Create Superuser
 │
 ▼
Application Live
```

---

# Security Features

* Environment Variables
* Hashed Passwords
* Django Authentication
* CSRF Protection
* Session Authentication
* Google OAuth Security
* Secure Production Deployment

---

# Lessons Learned

This project helped understand:

* Django Project Structure
* Authentication Systems
* Google OAuth Integration
* PostgreSQL Databases
* Production Deployment
* Environment Variables
* Django Signals
* User Management
* Admin Dashboards
* Debugging Production Issues
* Render Deployment Workflow

---

# Current Limitations

### Media Files

Render storage is temporary.

Uploaded profile images may disappear after redeployment.

### Planned Solution

Integrate:

* Cloudinary

for permanent image storage.

---

# Future Improvements

* Cloudinary Integration
* Password Reset via Email
* Email Verification
* Two-Factor Authentication
* User Activity Logs
* Better UI Design
* Dark/Light Theme
* REST API Version
* JWT Authentication
* Docker Support

---

# Project Status

Production Ready

Completed Features:

* Authentication System
* Google OAuth
* PostgreSQL Integration
* User Profiles
* Admin Dashboard
* Render Deployment

Future Work:

* Cloudinary Integration
* UI Improvements
* Additional Security Features

---

Developed as a learning project to understand real-world authentication systems and production deployment before integrating similar architecture into larger AI/ML applications.
