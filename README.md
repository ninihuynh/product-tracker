# skincare-inventory-web

# Skincare Inventory Web App

## Overview

This is a full-featured skincare inventory web application designed for salons to manage products, track purchases, and monitor stock levels efficiently.

---

## Features

- **User Authentication**: Secure login/register for staff and admins  
- **Product Management**: Add, edit, delete skincare products  
- **Inventory Tracking**: Real-time stock updates and purchase logging  
- **Stock Alerts**: Email notifications for low inventory  
- **Admin Dashboard**: Visualize stock levels and sales trends  
- **REST API**: JSON endpoints for integration  
- **Responsive UI**: Built with Bootstrap for desktop and mobile

---

## Technologies Used

| Technology      | Purpose                                 |
|-----------------|-----------------------------------------|
| Python          | Backend logic                          |
| Flask           | Web framework                         |
| SQLAlchemy      | ORM for database interactions         |
| Flask-Login     | User authentication                    |
| Flask-Mail      | Sending email notifications            |
| Flask-Migrate   | Database migrations                    |
| Bootstrap       | Frontend styling                       |
| SQLite/PostgreSQL | Persistent database                   |

---

## Installation

### 1. Clone repo

```bash
git clone git@github.com:ninihuynh/skincare-inventory-web.git
cd skincare-inventory-web
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

```bash
Create .env file:
FLASK_SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///site.db
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
```

### 5. Initialize database

```bash
flask db upgrade
```

### 6. Run the app

```bash
flask run
```

### 7. Open the browser

```bash
http://127.0.0.1:5000/
```


---

## How to Use

- Register an account and login
- Add skincare products with stock info
- Purchase products and watch inventory update
- Receive email alerts when stock runs low
- View purchase logs and reports






