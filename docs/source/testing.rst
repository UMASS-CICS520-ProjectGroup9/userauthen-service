Testing
=======

Test suite uses ``pytest`` with ``pytest-django`` and DRF's ``APIClient``.

Running the tests
-----------------

.. code-block:: console

   # From the repo root
   pytest -vv

What is covered
---------------
- Registration happy path and validation errors.
- Login via email (custom token), username (default SimpleJWT), and admin-only login.
- Token refresh flow.
- Authenticated profile retrieval and auth enforcement.
- Password change success and user-not-found cases.

Troubleshooting
---------------
- Ensure dependencies are installed (Django, djangorestframework, djangorestframework-simplejwt, pytest, pytest-django).
- If settings are not found, verify ``DJANGO_SETTINGS_MODULE=userauthen.settings`` (configured in ``pytest.ini``).
