# 🏪 Storefront API — Django REST Framework

A RESTful backend API for an e-commerce storefront, built with Django and the Django REST Framework (DRF). Designed to serve product data, manage orders, and handle customer interactions via a clean JSON API.

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL (configurable)
- **Architecture:** RESTful API

## Prerequisites

- Python 3.8+
- pip
- PostgreSQL (or SQLite for local dev)

## Getting Started

1. **Clone the repository**
```bash
   git clone https://github.com/phasetumurere/storefront.git
   cd storefront
```

2. **Create and activate a virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Configure environment** — update `settings.py` with your database credentials.

5. **Run migrations and start the server**
```bash
   python manage.py migrate
   python manage.py runserver
```

6. API is available at `http://localhost:8000/`

## API Overview

The API exposes endpoints for products, collections, orders, and customers — consumable by any frontend or mobile client.
