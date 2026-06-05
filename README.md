# Django Authentication System

A production-ready authentication system built with Django, PostgreSQL, Google OAuth, Cloudinary, and Render deployment.

---

# Live Demo

**Live Application:**

https://django-auth-project-i19m.onrender.com/

---

# Project Overview

This project was developed to learn and implement a complete production-ready authentication system before integrating similar architecture into larger AI/ML projects such as a Movie Recommendation System.

The project demonstrates real-world authentication workflows, user management, profile management, cloud storage integration, database deployment, and production deployment practices.

---

# Features

## Authentication

* User Registration
* User Login
* User Logout
* Session-Based Authentication
* Google OAuth Authentication
* Secure Password Hashing
* Protected Routes

---

## User Profile Management

* View Profile
* Edit Profile
* Update Bio
* Add GitHub Profile
* Add LinkedIn Profile
* Upload Profile Picture
* Automatic Profile Creation

---

## Dashboard

* View Total Users
* View Total Profiles
* View Active Users
* View Inactive Users
* View Staff Users
* View Registered Users
* User Details Page

---

## Admin Features

* Django Admin Panel
* User Management
* Profile Management
* Google OAuth Management
* Site Management
* Social Application Management

---

# Tech Stack

## Backend

* Django 6
* Django ORM
* Django Allauth

## Frontend

* HTML5
* CSS3
* Django Templates

## Database

### Development

* SQLite

### Production

* PostgreSQL

## Authentication

* Django Authentication System
* Django Allauth
* Google OAuth 2.0

## Cloud Storage

* Cloudinary

## Deployment

* Render
* Gunicorn
* WhiteNoise

## Environment Management

* Python Dotenv
* Environment Variables

---

# System Architecture

```text
                    ┌──────────────┐
                    │    User      │
                    └──────┬───────┘
                           │
                           ▼

                 Django Frontend Layer

                           │
                           │
        ┌──────────────────│──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼

 Authentication      User Profiles       Dashboard

        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼

                 Django Backend Logic

                           │
                           │
                           ▼

                 PostgreSQL Database

                           │
      ┌────────────────────┴────────────────────┐
      │                                         │
      ▼                                         ▼

 User Information                     Profile Images

 PostgreSQL                           Cloudinary
```

---

# Authentication Flow

## Manual Signup Flow

```text
User
 │
 ▼
Signup Form
 │
 ▼
Validate Data
 │
 ▼
Create User
 │
 ▼
Signal Triggered
 │
 ▼
Create Profile
 │
 ▼
Store In Database
 │
 ▼
Login User
 │
 ▼
Home Page
```

---

## Manual Login Flow

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
Redirect To Homepage
```

---

## Google OAuth Flow

```text
User
 │
 ▼
Continue With Google
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
 │
 ▼
Redirect To Homepage
```

---

# Database Design

## User Model

Django Built-in User Model

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

```text
Profile
 ├── user
 ├── bio
 ├── github
 ├── linkedin
 └── profile_picture
```

---

## Relationship

```text
User
 │
 └── One-To-One
         │
         ▼
      Profile
```

Each user owns exactly one profile.

---

# Automatic Profile Creation

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

# Project Structure

```text
django-auth-project/

│
├── accounts/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   ├── views.py
│   │
│   └── management/
│         └── commands/
│               └── create_superuser.py
│
│
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── profile.html
│   ├── edit_profile.html
│   ├── dashboard.html
│   └── user_detail.html
│
├── static/
│
├── requirements.txt
├── build.sh
├── manage.py
└── README.md
```

---

# Deployment Architecture

```text
GitHub
 │
 ▼

Render Deployment

 │

 ├── Install Dependencies
 ├── Run Migrations
 ├── Create Superuser
 ├── Collect Static Files
 ├── Start Gunicorn

 │

 ▼

Production Application

 │

 ├── PostgreSQL Database
 ├── Cloudinary Storage
 ├── WhiteNoise Static Files
 └── Google OAuth
```

---

# Environment Variables

The application uses environment variables to keep sensitive information secure.

```env
SECRET_KEY=

DEBUG=

ALLOWED_HOSTS=

DATABASE_URL=

SUPERUSER_USERNAME=

SUPERUSER_EMAIL=

SUPERUSER_PASSWORD=

GOOGLE_CLIENT_ID=

GOOGLE_CLIENT_SECRET=

CLOUDINARY_CLOUD_NAME=

CLOUDINARY_API_KEY=

CLOUDINARY_API_SECRET=
```

---

# Local Development Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Start Development Server

```bash
python manage.py runserver
```

---

# Production Deployment

Hosted on Render.

Deployment process:

```text
GitHub Push
      │
      ▼

Render Auto Deploy
      │
      ▼

Install Requirements
      │
      ▼

Run Migrations
      │
      ▼

Create Superuser
      │
      ▼

Collect Static Files
      │
      ▼

Start Gunicorn
      │
      ▼

Production Ready
```

---

# Security Features

* Environment Variables
* Hashed Passwords
* Django Authentication
* Session Authentication
* CSRF Protection
* Google OAuth Security
* PostgreSQL Database Security
* Secure Production Deployment

---

# Challenges Solved

During development and deployment, the following real-world problems were solved:

* Google OAuth Configuration
* OAuth Redirect URI Issues
* Django Allauth Integration
* PostgreSQL Migration
* Environment Variable Management
* Render Deployment Issues
* Cloudinary Integration
* Static Files Configuration
* Production Media Storage
* User Profile Automation
* Superuser Creation On Render
* Local vs Production Configuration Management
* Database Synchronization
* Social Application Configuration

---

# Lessons Learned

This project provided practical experience with:

* Django Project Structure
* Authentication Systems
* Google OAuth
* PostgreSQL
* Cloudinary
* Django Signals
* Production Deployment
* Render Hosting
* Environment Variables
* User Management
* Dashboard Development
* Debugging Production Issues
* Full Stack Web Development

---

# Future Improvements

* Password Reset Via Email
* Email Verification
* Two-Factor Authentication (2FA)
* User Activity Tracking
* Dark Mode
* Better UI/UX Design
* REST API Integration
* JWT Authentication
* Docker Containerization
* CI/CD Pipeline
* Role-Based Access Control

---

# Project Status

## Version

v1.0

## Status

Production Ready

## Completed Features

* Authentication System
* Google OAuth
* PostgreSQL Integration
* Cloudinary Integration
* User Profiles
* Automatic Profile Creation
* Admin Dashboard
* Django Admin Panel
* Environment Variables
* Render Deployment

---

# Key Takeaway

This project was created as a learning milestone before integrating production-grade authentication into larger AI/ML applications.

The architecture developed here can be directly reused in future projects such as:

* Movie Recommendation Systems
* AI Applications
* SaaS Products
* E-Commerce Platforms
* Social Platforms

By completing this project, I gained hands-on experience with real-world authentication, cloud storage, database deployment, and production debugging workflows.

---

**Developed using Django, PostgreSQL, Google OAuth, Cloudinary, and Render.**
