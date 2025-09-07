# 🏗 Gimme What Lee Got

**Gimme What Lee Got** is a playful yet ambitious project inspired by the RDCworld “Lee” meme.  
It’s a **full-stack catalog & recommendation platform** built to explore **Django, REST APIs, modern frontend, and AI/ML concepts**.  

---

## 🚀 Tech Stack

### Backend
- **Django** → web framework  
- **Django REST Framework (DRF)** → REST APIs  
- **PostgreSQL** → main database  
- **django-environ** → environment variables & secrets  
- **JWT (SimpleJWT)** → authentication  

### Frontend
- **React + TypeScript** → interactive UI  
- **Vite** → fast dev server and bundler  
- **Axios / Fetch** → API calls  
- **CSS / Assets** → styling  

---

## ⚙️ How to Run Locally

### 1 Clone the repository
```bash
git clone https://github.com/ramyozi/gimmewhatleegot.git
cd gimmewhatleegot
```

### 2 Backend setup (Django + PostgreSQL)
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

# Install dependencies
```bash
pip install -r requirements.txt
```

Important: 
- Create a .env file in the project root (next to manage.py) based on .env.example
- Make sure PostgreSQL is installed and running, and the database/user exist:
(createdb gimmewhatleegot)
- Run migrations and start the backend:
```bash
python manage.py migrate
python manage.py runserver
```

Backend will be available at: http://127.0.0.1:8000

### 3️⃣ Frontend setup (React + Vite)
```bash
cd frontend
npm install
```
Create a .env file inside frontend/ based on .env.example.
Start the frontend: 
```bash
npm run dev
```
Frontend will be available at: http://127.0.0.1:3000


---
# What is this project and why:

## Gimme What Lee Got

**Gimme What Lee Got** is a playful yet ambitious project inspired by the RDCworld “Lee” meme.
The idea is simple: just like Mark asked the barber to "give me what Lee got", this app helps people discover and get recommendations for products, services, or content that others have found useful, interesting, or popular.

### Goal of the Project
The goal is to build a smart catalog and recommendation platform powered by:
- Django + Django REST Framework → backend & APIs
- React (or any modern frontend) → interactive UI
- PostgreSQL → structured, reliable data storage
- AI/ML models → personalized recommendations ("give me what Lee got, but smarter")

### Concept
Instead of being just a static library or marketplace, **Gimme What Lee Got** focuses on:
- Cataloging: Store and organize products/services/content.
- Recommendations: Suggest items to users based on what others like, trends, or similarity (AI-driven).
- Community-driven discovery: If Lee liked it, maybe you will too.

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



