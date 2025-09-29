# Library Management System (Django)

A simple library application built with **pure Django and function-based views**.  
This project was created as part of a machine test assignment.

---

## 📦 Features Implemented

- **Books Management**
  - List all books with search (by title/author) and pagination
  - Book detail page with availability info

- **Borrowing System**
  - Borrow books (max 3 active borrowings per user)
  - Prevent borrowing the same book twice until returned
  - Default loan period = 14 days
  - Return borrowed books

- **User Dashboard**
  - "My Borrowings" page with Active and History tabs
  - Overdue borrowings highlighted

- **Authentication**
  - Login & Logout (Django’s built-in auth)
  - User signup/registration form

- **Feedback**
  - Success & error messages shown via Django messages

- **Admin**
  - Manage books and borrowings in Django Admin
  - Useful list displays and filters

---

## ⚙️ Tech Stack

- Python 3.13
- Django 5.x
- SQLite (default database)
- Bootstrap 5 (via CDN)

---


