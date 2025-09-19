# 🛠️ Gimme What Lee Got – Backend

This is the **backend API** for **Gimme What Lee Got**, built with **Django + Django REST Framework (DRF)**.
It powers the catalog, authentication, and recommendation logic.

---

## 🚀 Tech Stack

- **Django** – web framework
- **Django REST Framework (DRF)** – REST APIs
- **PostgreSQL** – main database
- **django-environ** – environment variables
- **SimpleJWT** – JWT-based authentication

---

## ⚙️ Setup & Run Locally

### 1) Clone the repository

```bash
git clone https://github.com/ramyozi/gimmewhatleegot-backend.git
cd gimmewhatleegot-backend
```

### 2) Create & activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment

Create a .env file in the project root (next to manage.py) based on .env.example:

```bash
SECRET_KEY=your_django_secret
DEBUG=True
DATABASE_NAME=gimmewhatleegot
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=xxxx
```

### 4) Setup database

Make sure PostgreSQL is running, then:

```bash
createdb gimmewhatleegot
python manage.py migrate
```

### 4) Run backend

```bash
python manage.py runserver
```

Backend will be available at: http://127.0.0.1:8000

## Project Structure

```
gimmewhatleegot-backend/
├── catalog/         # Items, categories, interactions
├── users/           # Authentication, registration
├── core/           # Settings, urls, wsgi
└── requirements.txt
```

---

# What is this project and why:

## Gimme What Lee Got

**Gimme What Lee Got** is a playful yet ambitious project inspired by the RDCworld “Lee” meme.
The idea is simple: just like Mark asked the barber to "give me what Lee got", this app helps people discover and get recommendations for books, comics, and other content that others have found useful, interesting, or popular.

### Goal of the Project

The goal is to build a smart catalog and recommendation platform powered by:

- Django + Django REST Framework → backend & APIs
- React (or any modern frontend) → interactive UI
- PostgreSQL → structured, reliable data storage
- AI/ML models → personalized recommendations ("give me what Lee got, but smarter")

### Concept

Instead of being just a static library or marketplace, **Gimme What Lee Got** focuses on:

- Cataloging: Store and organize a wide range of items including products, books, comics, articles, services, and media content.
- Recommendations: Suggest items to users based on what others like, trends, or similarity (AI-driven).
- Community-driven discovery: If Your friend liked it, maybe you will too.

### Why this project?

This repo is more than just code. It’s my learning journey into:

- Django & backend architecture
- REST APIs & frontend integration
- Database design with PostgreSQL
- AI-powered recommendation systems

### Vision

Over time, the project could evolve into:

- A platform for personalized discovery (like Netflix for products/services).
- A tool for teams or individuals to showcase and share curated items.
- A space where "give me what Lee got" isn’t just a joke — it’s a smart way to find what you need.

---

This is a learning project. The focus is on exploring Django, AI, and full-stack development while building something fun and useful.

