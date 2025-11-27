# Events Service API (User Authentication)

This project exposes the user authentication layer for the Events service API. It is built with Django, Django REST Framework, and SimpleJWT, providing JWT-based login, registration, and role-aware access for admins, staff, and students.

## Overview
- Custom user model with roles (ADMIN, STAFF, STUDENT).
- Email- or username-based authentication with JWT access/refresh tokens.
- Admin-only token issuance endpoint.
- Profile retrieval and password change endpoints.

## Documentation
- Sphinx docs live under `docs/`. Build with `cd docs && make html` and open `docs/build/html/index.html`.
- Key pages: overview, API endpoints, and testing instructions.

## How to Compile and Run
1) Install dependencies:
```bash
pip install -r requirements.txt
```
2) Apply migrations (uses SQLite by default):
```bash
python manage.py migrate
```
3) Start the development server:
```bash
python manage.py runserver
```

## Python Version and Environment
- Tested with Python 3.11.
- Recommended: create a virtual environment (`python -m venv .venv && source .venv/bin/activate`) before installing packages.

## Features
- User registration with username/email/password/role.
- JWT issuance via email/password or username/password.
- Token refresh endpoint.
- Admin-only login endpoint with staff/superuser enforcement.
- Authenticated profile endpoint.
- Password change by email.

## Testing
Run the automated test suite (pytest + pytest-django):
```bash
pytest -vv
```

## Project Structure
- `userauthen/` – Django project config, URLs, views, serializers.
- `users/` – Custom user model and tests.
- `docs/` – Sphinx documentation sources.
- `manage.py` – Django entrypoint.
- `db.sqlite3` – Default SQLite database (development).

## Authentication
- JWT Bearer tokens via `djangorestframework-simplejwt`.
- Custom email-based login at `/api/token/`; default SimpleJWT login at `/api/login/`.
- Admin-only login at `/api/admin-login/` (requires `is_staff` or `is_superuser`).

## API Endpoints (/api/)
- `POST /api/register/` – create user.
- `POST /api/login/` – username/password login (SimpleJWT default).
- `POST /api/token/` – email/password login with role in tokens.
- `POST /api/token/refresh/` (alias `/api/refresh/`) – refresh access token.
- `GET /api/profile/` – authenticated user profile.
- `POST /api/admin-login/` – admin/staff-only token issuance.
- `PUT /api/changepwd/` – change password by email.
