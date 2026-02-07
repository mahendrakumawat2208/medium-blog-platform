# Medium-like Blog Platform

A full-stack blog platform inspired by Medium: write and publish stories, follow authors, and read a personalized feed.

## Stack

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, JWT auth
- **Frontend:** Next.js 16, React 19, Tailwind CSS

## Quick start

### 1. Database (PostgreSQL)

Using Docker:

```bash
docker compose up -d
```

Or use your own Postgres and set `DATABASE_URL` in `backend/.env`.

### 2. Backend

```bash
cd backend
cp .env.example .env   # edit if needed
python -m venv .venv
source .venv/bin/activate   # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API runs at **http://localhost:8000**. Docs: http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at **http://localhost:3000**. Set `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1` in `.env.local` if your API is elsewhere.

## Features

- **Auth:** Register, login, JWT
- **Posts:** Create (draft/publish), edit, delete, view by slug
- **Feed:** Latest posts; when logged in, feed from people you follow
- **Profiles:** View user profile and posts, follow/unfollow
- **Write:** New story with title and body (markdown-friendly)

## Git

This repo is set up for Git. To push to your GitHub:

1. Create a new repository on GitHub (e.g. `medium-blog-platform`).
2. Add the remote and push:

   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/medium-blog-platform.git
   git branch -M main
   git push -u origin main
   ```

Use your GitHub account (e.g. mahendrakumawat2208@gmail.com) when signing in to GitHub to push.
