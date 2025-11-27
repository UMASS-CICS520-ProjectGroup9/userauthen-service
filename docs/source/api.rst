API Endpoints
=============

Authentication
--------------

Custom email login
~~~~~~~~~~~~~~~~~~
- **POST** ``/api/token/``
- Body:

  .. code-block:: json

     {
       "email": "user@example.com",
       "password": "hunter2"
     }

- Success (``200``):

  .. code-block:: json

     {
       "refresh": "<refresh>",
       "access": "<access>",
       "user_id": 1,
       "email": "user@example.com",
       "role": "STUDENT"
     }

- Errors: ``400`` with ``"Invalid email or password"``.

Username login (default SimpleJWT)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **POST** ``/api/login/``
- Body: ``{"username": "<username>", "password": "<password>"}``
- Success: returns ``refresh`` and ``access`` tokens.

Admin login
~~~~~~~~~~~
- **POST** ``/api/admin-login/``
- Only for staff/superusers.
- Body: ``{"username": "<admin>", "password": "<password>"}``
- Success (``200``): refresh/access plus ``username``, ``is_staff``, ``is_superuser``.
- Failure (``400``): ``{"detail": "Only admin users can log in here."}``

Token refresh
~~~~~~~~~~~~~
- **POST** ``/api/token/refresh/`` (or ``/api/refresh/``)
- Body: ``{"refresh": "<refresh token>"}``
- Success: ``{"access": "<new access token>"}``

Registration
------------
- **POST** ``/api/register/``
- Body:

  .. code-block:: json

     {
       "username": "newuser",
       "email": "newuser@example.com",
       "password": "StrongPass123!",
       "role": "STUDENT"
     }

- Success (``201``): newly created user fields (id/username/email/role).
- Validation errors: ``400`` with field-level errors.

Profile
-------
- **GET** ``/api/profile/``
- Requires ``Authorization: Bearer <access>``.
- Success (``200``):

  .. code-block:: json

     {
       "id": 1,
       "username": "newuser",
       "email": "newuser@example.com"
     }

- Unauthenticated: ``401``.

Password change
---------------
- **PUT** ``/api/changepwd/``
- Body:

  .. code-block:: json

     {
       "email": "user@example.com",
       "password": "NewStrongPass!"
     }

- Success (``200``): ``{"detail": "Password updated successfully"}``
- User missing: ``404`` with ``{"error": "User not found"}``
