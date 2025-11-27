import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_password():
    return "TestPass123!"


@pytest.fixture
def student_user(django_user_model, user_password):
    return django_user_model.objects.create_user(
        username="student",
        email="student@example.com",
        password=user_password,
        role="STUDENT",
    )


@pytest.fixture
def admin_user(django_user_model, user_password):
    return django_user_model.objects.create_user(
        username="admin",
        email="admin@example.com",
        password=user_password,
        role="ADMIN",
        is_staff=True,
        is_superuser=True,
    )


@pytest.mark.django_db
def test_register_user_success(api_client):
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "role": "STUDENT",
        "password": "NewPass123!",
    }

    response = api_client.post("/api/register/", payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == payload["username"]
    assert response.data["email"] == payload["email"]
    assert response.data["role"] == payload["role"]
    assert "password" not in response.data


@pytest.mark.django_db
def test_register_user_missing_fields(api_client):
    response = api_client.post(
        "/api/register/",
        {"username": "incomplete", "role": "STUDENT"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data


@pytest.mark.django_db
def test_login_with_email_token_pair(api_client, student_user, user_password):
    response = api_client.post(
        "/api/token/",
        {"email": student_user.email, "password": user_password},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert {"refresh", "access", "user_id", "email", "role"} <= set(
        response.data.keys()
    )
    assert response.data["email"] == student_user.email


@pytest.mark.django_db
def test_login_with_email_invalid_credentials(api_client, student_user):
    response = api_client.post(
        "/api/token/",
        {"email": student_user.email, "password": "wrongpass"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_refresh_token(api_client, student_user, user_password):
    login = api_client.post(
        "/api/token/",
        {"email": student_user.email, "password": user_password},
        format="json",
    )
    refresh_token = login.data["refresh"]

    response = api_client.post(
        "/api/token/refresh/", {"refresh": refresh_token}, format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_profile_requires_authentication(api_client):
    response = api_client.get("/api/profile/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_profile_returns_user_data(api_client, student_user, user_password):
    login = api_client.post(
        "/api/token/",
        {"email": student_user.email, "password": user_password},
        format="json",
    )
    access_token = login.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.get("/api/profile/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == student_user.id
    assert response.data["username"] == student_user.username
    assert response.data["email"] == student_user.email


@pytest.mark.django_db
def test_change_password_updates_password(api_client, student_user):
    new_password = "UpdatedPass456!"

    response = api_client.put(
        "/api/changepwd/",
        {"email": student_user.email, "password": new_password},
        format="json",
    )

    student_user.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert response.data["detail"] == "Password updated successfully"
    assert student_user.check_password(new_password)


@pytest.mark.django_db
def test_change_password_user_not_found(api_client):
    response = api_client.put(
        "/api/changepwd/",
        {"email": "missing@example.com", "password": "DoesNotMatter"},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "User not found"


@pytest.mark.django_db
def test_admin_login_success(api_client, admin_user, user_password):
    response = api_client.post(
        "/api/admin-login/",
        {"username": admin_user.username, "password": user_password},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert {"refresh", "access", "username", "is_staff", "is_superuser"} <= set(
        response.data.keys()
    )
    assert response.data["is_staff"] is True
    assert response.data["is_superuser"] is True


@pytest.mark.django_db
def test_admin_login_rejects_non_admin(api_client, student_user, user_password):
    response = api_client.post(
        "/api/admin-login/",
        {"username": student_user.username, "password": user_password},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Only admin users can log in here." in str(response.data["detail"])


@pytest.mark.django_db
def test_default_login_with_username(api_client, student_user, user_password):
    response = api_client.post(
        "/api/login/",
        {"username": student_user.username, "password": user_password},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert {"refresh", "access"} <= set(response.data.keys())
