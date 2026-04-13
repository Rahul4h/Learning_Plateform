# Interactive Teaching Platform

This repository contains a clean backend-first project structure for an interactive teaching platform where article text can trigger contextual multimedia content.

## What This Project Does

- Serves article-based learning content
- Supports clickable highlights inside article text
- Opens context-aware content such as text, image, audio, or YouTube media
- Exposes structured sidebar sections like introduction, explanation, and resources

## Recommended Stack

- Python 3.12+
- Django
- Django REST Framework
- PostgreSQL
- Cloudinary or S3 for media in production

## Suggested Folder Structure

```text
backend/
  config/
    __init__.py
    settings.py
    urls.py
    asgi.py
    wsgi.py
  apps/
    common/
      __init__.py
      constants.py
    articles/
      __init__.py
      apps.py
      admin.py
      models.py
      serializers.py
      views.py
      urls.py
      services.py
      tests.py
    highlights/
      __init__.py
      apps.py
      admin.py
      models.py
      serializers.py
      views.py
      urls.py
      tests.py
    sections/
      __init__.py
      apps.py
      admin.py
      models.py
      serializers.py
      views.py
      urls.py
      tests.py
docs/
  architecture.md
```

## Design Principle

Keep the system article-centric:

- `Article` owns the main content
- `Highlight` points to exact article phrases and their related media
- `Section` powers the right sidebar accordion

## Recommended API Shape

- `GET /api/articles/`
- `GET /api/articles/{id}/`
- `GET /api/articles/{id}/highlights/`
- `GET /api/articles/{id}/sections/`

For frontend performance, the article detail endpoint can also embed both highlights and sections.

## Next Build Step

Start implementation from these files first:

1. `backend/apps/articles/models.py`
2. `backend/apps/highlights/models.py`
3. `backend/apps/sections/models.py`
4. `backend/config/settings.py`
5. `backend/config/urls.py`

## Step By Step Run Guide

1. Create a virtual environment
2. Activate it
3. Install dependencies from `requirements.txt`
4. Copy `.env.example` values into your local environment
5. Run migrations
6. Create a superuser
7. Start the development server

Example commands:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## GitHub Push Guide

```powershell
cd "F:\Rahul alternative\DRF\New project"
git init
git add .
git commit -m "Initial interactive learning platform"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

## Deployment Notes

Recommended free-first deployment path:

- App: Render
- Database: Render PostgreSQL or external PostgreSQL provider

Environment variables needed in deployment:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=<your-render-domain>`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

Recommended production changes before public deployment:

- use `gunicorn` instead of `runserver`
- add WhiteNoise or another static file strategy
- use strong database credentials
- disable debug mode
