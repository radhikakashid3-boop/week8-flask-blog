# My Personal Blog

A professional personal blog web application built with Python Flask.

## Features

- User registration and login
- Secure password hashing
- Logout
- Forgot password
- Password reset tokens
- Create blog posts
- Edit own posts
- Delete own posts
- View published posts
- Comments
- Delete own comments
- Search by title and content
- Pagination
- CSRF protection
- SQLite database
- SQLAlchemy ORM
- Flask-Migrate
- Bootstrap responsive UI
- Custom 404 and 500 pages
- Automated tests

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Migrate
- SQLite
- Jinja2
- Bootstrap
- HTML
- CSS
- JavaScript
- Pytest

## Project Structure

```text
week8-flask-blog/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   │
│   ├── auth/
│   ├── main/
│   ├── posts/
│   ├── comments/
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
├── migrations/
├── templates/
├── tests/
├── config.py
├── run.py
├── README.md
├── requirements.txt
└── .gitignore
