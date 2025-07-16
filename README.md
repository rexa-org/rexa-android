# reX (Reward Exchange)

A modern platform to consolidate, exchange, and monetize digital rewards (cashback, vouchers, scratch cards) from apps like GPay, PhonePe, Paytm, and more.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Backend (FastAPI)](#backend-fastapi)
  - [Frontend (React Native)](#frontend-react-native)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Running Dev Servers](#running-dev-servers)
- [Testing](#testing)
- [Deployment](#deployment)

---
## Project Overview
reX lets users scan, manage, exchange, and sell digital rewards from multiple apps, with privacy-first scraping and a global marketplace. Admins can moderate listings and view commission reports.

## Tech Stack
- **Mobile:** React Native (Expo), TypeScript, React Navigation, Native Android modules
- **Backend:** FastAPI, Python 3.10+, SQLAlchemy, Alembic, PostgreSQL
- **Auth:** JWT (access/refresh), bcrypt
- **Payments:** Razorpay (India), Stripe (optional)
- **Storage:** S3/Cloudinary (optional)
- **DevOps:** Docker, GitHub Actions, .env

## Prerequisites
- Node.js >= 18
- Python >= 3.10
- Docker & Docker Compose
- PostgreSQL (local or cloud)

---

## Setup

### Backend (FastAPI)
1. **Clone the repo:**
   ```bash
   git clone <repo-url>
   cd rexa-android/backend
   ```
2. **Copy and edit environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your DB, JWT, and API keys
   ```
3. **Run with Docker:**
   ```bash
   docker build -t rex-backend .
   docker run --env-file .env -p 8000:8000 rex-backend
   ```
   Or run locally:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

### Frontend (React Native)
1. **Install dependencies:**
   ```bash
   cd ../mobile
   npm install
   ```
2. **Start Expo dev server:**
   ```bash
   npm start
   # Or: npx expo start
   ```
3. **Run on device/emulator:**
   - Android: `npm run android`
   - iOS: `npm run ios`

---

## Environment Variables
See `.env.example` for all required variables:
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - JWT signing secret
- `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` - Razorpay API keys
- `S3_BUCKET`, `S3_KEY`, `S3_SECRET` - (optional) S3 storage
- `ADMIN_EMAIL`, `SECRET_KEY` - Admin and session secrets

---

## Database Migrations
1. **Initialize Alembic (if not done):**
   ```bash
   alembic init alembic
   ```
2. **Edit `alembic.ini` and `env.py` for your DB URL.**
3. **Create migration:**
   ```bash
   alembic revision --autogenerate -m "init"
   ```
4. **Apply migration:**
   ```bash
   alembic upgrade head
   ```

---

## Running Dev Servers
- **Backend:**
  ```bash
  cd backend
  uvicorn app.main:app --reload
  ```
- **Frontend:**
  ```bash
  cd mobile
  npm start
  ```

---

## Testing
- **Backend:**
  ```bash
  pytest
  ```
- **Frontend:**
  ```bash
  npm test
  ```
- **CI:**
  - Lint: `flake8`, `black`
  - Tests: `pytest`, `jest`

---

## Deployment
- **Backend:** Deploy Docker image to Railway/Render.
- **Frontend:** Use Expo/EAS for builds and Play Store publishing.
- **CI/CD:** GitHub Actions for lint, test, build, and deploy.

---

## Notes
- No hard-coded secrets. Use `.env` for all sensitive config.
- Scraping modules are opt-in and battery-efficient.
- UI uses a consistent design system (customizable).
- Modular: OCR, accessibility, and storage can be disabled.
