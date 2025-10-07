# Food Distribution Business Platform

[![Python](https://img.shields.io/badge/python-%3E%3D3.8-blue)]()

A Django-based web application for restaurant and food delivery management. It allows you to create and organize menus, manage daily deals, and process customer orders. The admin interface provides tools for content management, order monitoring, and system configuration. The project uses Django templates for frontend rendering, static assets for styling and interactivity, and a modular Python backend to handle business logic. The full stack involves Python, Django, HTML, CSS, and JavaScript.

---

## Overview

Food Distribution Business Platform enables users to:
- Manage **menus** and **products**
- Handle **customer orders** efficiently
- Generate and track **invoices**
- Update **website content** through a built-in CMS
- Improve **SEO** and manage metadata
- Receive **automated email notifications** for orders and account activity

---

## Features

- **Invoicing System**: Automatically create and manage invoices for customer orders.  
- **Ordering System**: Track and manage customer orders in real time.  
- **CRM (Customer Relationship Management)**: Store customer information and track order history.  
- **CMS (Content Management System)**: Update website content without touching the code.  
- **SEO-Friendly Design**: Enhance search engine visibility.  
- **Automated Email Notifications**: Send order confirmations and account alerts automatically.

---

## Tech Stack

- **Backend:** Django 4.x+  
- **Frontend:** HTML, CSS, JavaScript (Django templates)  
- **Database:** SQLite / PostgreSQL  
- **Email:** SMTP or third-party email services  
- **Other Libraries:** As listed in `requirements.txt`  

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Lachi1921/Food-Distribution/
cd lunch.pk
````

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

* **Windows:**

```bash
venv\Scripts\activate
```

* **macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set up environment variables

Create a `.env` file in the project root with values like:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
```

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## Usage

* Access the **Admin Dashboard** at `/admin` to manage:

  * Menu items
  * Orders
  * Customers
  * Website content

* Extend the system to include additional features like delivery services, automated billing, or reporting tools.
