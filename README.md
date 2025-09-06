# 💼 Job Tracker

A full-stack web app to manage job applications, built with **Next.js, Django REST Framework, and PostgreSQL**.
Track applications, contacts, tasks, and interview stages with a clean dashboard, kanban pipeline, and searchable tables.

[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js)](https://nextjs.org/)

[![Django REST](https://img.shields.io/badge/Django%20REST-API-green?logo=django)](https://www.django-rest-framework.org/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Features

- 🔐 Authentication (JWT with access/refresh tokens)
- 📊 Dashboard with KPIs (applications, interviews, offers, rejections)
- 🗂 Applications table with filters, search, pagination, CSV export
- 📌 Kanban board (Applied → Interview → Offer → Rejected) 🚧 _(work in progress)_
- 📇 Application detail with contacts & tasks
- ⚙️ User settings (profile, password, export, delete account)
- 🌐 Responsive, modern SaaS UI (Next.js + shadcn/ui + Tailwind)

---

## 🛠️ Tech Stack

### Frontend

- Next.js (App Router, TypeScript)
- React Query for server state
- shadcn/ui + Tailwind CSS
- Zod + React Hook Form for validation
- dnd-kit for drag-and-drop

### Backend

- Django + DRF
- PostgreSQL
- SimpleJWT for auth
- django-filter

### Infra / Tooling

- Docker & docker-compose
- GitHub Actions (CI/CD)
- Prettier, ESLint, Black

---

## 🏃‍♂️ Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker (optional)

### Installation

```bash
# clone repo
git clone https://github.com/Hayisul/job-tracker.git
cd job-tracker

# frontend
cd apps/web
npm install
npm run dev

# backend
cd ../api
python -m venv venv && source venv/bin/activate

# install deps (until requirements.txt is added)
pip install django djangorestframework django-filter djangorestframework-simplejwt corsheaders python-dotenv

python manage.py migrate
python manage.py runserver
```

## 📦 Deployment

- Frontend → Vercel
- Backend → Render / Railway

## 🖥️ Usage

1. Register a new account or log in
2. Add job applications, contacts, and tasks
3. Move applications through the kanban pipeline
4. Search and filter information as needed

## 💡 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📜 License

This project is licensed under the MIT License.
