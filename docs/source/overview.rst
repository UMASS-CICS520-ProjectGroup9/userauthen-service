Overview
========

This service provides user authentication and authorization APIs for a Django project.
It uses Django REST Framework (DRF) and `djangorestframework-simplejwt` for JWT-based auth.

Key features
------------
- JWT access/refresh token issuance for normal users.
- Admin-only token endpoint to restrict privileged logins.
- Profile lookup for the authenticated user.
- Password change by email.

Architecture
------------
- Django 5 + DRF for API endpoints.
- Custom user model ``users.CustomUser`` with a ``role`` field (``ADMIN``, ``STAFF``, ``STUDENT``).
- Email-based authentication backend for the custom token endpoint.
- SimpleJWT configured with Bearer tokens.

API surface (quick glance)
--------------------------
- ``POST /api/register/``: create account (username, email, password, role).
- ``POST /api/login/``: default SimpleJWT login with ``username``/``password``.
- ``POST /api/token/``: custom login with ``email``/``password`` returning ``role`` in tokens.
- ``POST /api/token/refresh/``: refresh access token.
- ``GET /api/profile/``: authenticated profile of the current user.
- ``POST /api/admin-login/``: token issuance restricted to staff/superusers.
- ``PUT /api/changepwd/``: change password by email.
