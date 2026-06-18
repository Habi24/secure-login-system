# Secure Login System

A secure login system built using Flask, SQLite, and bcrypt.

## Features

* User Registration
* User Login Authentication
* Password Hashing using bcrypt
* Input Validation
* SQL Injection Protection
* Session Management
* Logout Functionality
* Responsive User Interface

## Technologies Used

* Python
* Flask
* SQLite
* bcrypt
* HTML
* CSS

## Project Structure

```
secure-login-system/
│
├── app.py
├── create_db.py
├── templates/
├── static/
└── .gitignore
```

## Security Features

* Passwords are stored as bcrypt hashes.
* SQL Injection is prevented using parameterized queries.
* Session-based authentication is implemented.
* Input validation is performed for user credentials.
