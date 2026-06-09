# 🚀 Django Authentication System

A production-ready authentication platform built with **Django**, **PostgreSQL**, **Google OAuth**, **Cloudinary**, and **Render**.

This project demonstrates how modern web applications handle authentication, user management, profile management, cloud media storage, third-party OAuth integration, and production deployment.

---

## 🌐 Live Demo

**Application URL**

https://django-auth-project-i19m.onrender.com/

---

## 📖 Project Overview

This project was built as a foundation for future AI/ML and SaaS applications.

Before integrating authentication into larger systems such as recommendation engines, AI assistants, or machine learning platforms, I wanted to build and understand a complete authentication workflow from development to production deployment.

The application includes:

* Traditional Username/Password Authentication
* Google OAuth Authentication
* User Profile Management
* Cloud-Based Media Storage
* PostgreSQL Database Integration
* Admin Analytics Dashboard
* Production Deployment Pipeline

The architecture follows real-world development practices and can be reused directly in future projects.

---

# ✨ Features

## 🔐 Authentication System

* User Registration
* User Login
* User Logout
* Session Authentication
* Password Hashing
* Route Protection
* Google OAuth Login
* Secure User Sessions

---

## 👤 User Profile Management

* View Profile
* Edit Profile
* Upload Profile Picture
* Bio Management
* GitHub Integration
* LinkedIn Integration
* Automatic Profile Creation
* Cloudinary Media Storage

---

## 📊 Admin Dashboard

* Total Users Analytics
* Active Users Analytics
* Staff Users Analytics
* Profile Statistics
* User Management Dashboard
* User Detail Pages
* Interactive Analytics Charts
* Search Registered Users

---

## ☁️ Cloud Integration

* Cloudinary Image Storage
* Google OAuth Authentication
* PostgreSQL Production Database

---

## 🚀 Deployment Features

* Render Deployment
* Gunicorn Production Server
* WhiteNoise Static File Management
* Environment Variable Management
* Automated Database Migrations
* Automated Superuser Creation

---

# 🛠 Tech Stack

## Backend

* Django 6
* Django ORM
* Django Signals
* Django Allauth

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Chart.js

## Database

### Development

* SQLite

### Production

* PostgreSQL

## Authentication

* Django Authentication System
* Django Allauth
* Google OAuth 2.0

## Media Storage

* Cloudinary

## Deployment

* Render
* Gunicorn
* WhiteNoise

## Configuration

* Python Dotenv
* Environment Variables

---

# 🏗 System Architecture

```text
                         ┌──────────────────┐
                         │      USER        │
                         └────────┬─────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │       Django Frontend      │
                    └─────────────┬──────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼

 Authentication            User Profiles            Dashboard

        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │      Django Backend        │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │      PostgreSQL DB         │
                    └─────────────┬──────────────┘
                                  │
              ┌───────────────────┴───────────────────┐
              │                                       │
              ▼                                       ▼
      User Data Storage                          Media Storage
      
         PostgreSQL                               Cloudinary
```

---

# 🔄 Authentication Flow

## Manual Authentication

```text
User
 │
 ▼
Signup Form
 │
 ▼
Validate Input
 │
 ▼
Create User
 │
 ▼
Django Signal
 │
 ▼
Create Profile
 │
 ▼
Store In Database
 │
 ▼
Authenticate User
 │
 ▼
Homepage
```

---

## Google OAuth Authentication

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
Grant Permission
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
Authenticate User
 │
 ▼
Homepage
```

---

# 🗄 Database Design

## User Model

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

## Profile Model

```text
Profile
├── user
├── profile_picture
├── bio
├── github
└── linkedin
```

### Relationship

```text
User
 │
 └── One-To-One
        │
        ▼
     Profile
```

Each authenticated user owns exactly one profile.

---

# ⚡ Automatic Profile Creation

The application uses Django Signals.

```text
User Created
      │
      ▼
Signal Triggered
      │
      ▼
Profile Created
      │
      ▼
Database Updated
```

This guarantees every user always has an associated profile.

---

# 📁 Project Structure

```text
django-auth-project
│
├── accounts/
│   ├── management/
│   │   └── commands/
│   │       └── create_superuser.py
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/
│
├── static/
│
├── build.sh
├── requirements.txt
├── manage.py
└── README.md
```

---

# ☁️ Production Deployment Architecture

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

   ├── PostgreSQL
   ├── Cloudinary
   ├── Google OAuth
   └── WhiteNoise
```

---

# 🔒 Security Features

* Environment Variables
* Hashed Password Storage
* CSRF Protection
* Session Authentication
* Secure Google OAuth
* Production Database Security
* Protected Routes
* Django Security Middleware

---

# 🧩 Problems Solved During Development

* Google OAuth Configuration
* OAuth Redirect URI Errors
* Django Allauth Integration
* Cloudinary Media Storage Migration
* PostgreSQL Migration Issues
* Environment Variable Management
* Render Deployment Configuration
* Production Static Files Management
* Automatic Profile Creation
* Automated Superuser Creation
* Local vs Production Configuration
* Social Application Configuration

---

# 📚 Key Learning Outcomes

* Django Authentication Internals
* OAuth 2.0 Integration
* Production Deployment Workflows
* PostgreSQL Management
* Cloudinary Integration
* Django Signals
* Full-Stack Development
* Production Debugging
* Secure Configuration Management
* User Management Systems

---

# 🔮 Future Improvements

* Email Verification
* Password Reset via Email
* Two-Factor Authentication (2FA)
* JWT Authentication
* REST API Support
* Docker Containerization
* CI/CD Pipeline
* Role-Based Access Control (RBAC)
* User Activity Logs
* Audit Trail System

---

# 📌 Project Status

**Version:** v1.0

**Status:** Production Ready ✅

---

# 👨‍💻 Developer

**Ayush Pratap Singh**

Passionate about AI, Machine Learning, Deep Learning, and Full-Stack Development.

This authentication system serves as the foundation for future AI-powered applications and SaaS products.

---

⭐ If you found this project helpful, consider giving it a star.
