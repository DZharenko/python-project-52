import types

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from task_manager.rollbar_middleware import CustomRollbarNotifierMiddleware


def dummy_get_response(request):
    return None


# Rollbar fixture
@pytest.fixture(autouse=True)
def enable_rollbar():
    settings.ROLLBAR = {"access_token": "test_token"}


@pytest.mark.django_db
class TestUsers:

    # Test Index
    def test_index_view(self, client):
        url = reverse("users")
        response = client.get(url)
        assert response.status_code == 200
        templates = [t.name for t in response.templates if t.name]
        assert "users/index.html" in templates

    # Test Create User
    def test_user_registration(self, client):
        url = reverse("user_create")
        data = {
            "username": "newuser",
            "first_name": "First",
            "last_name": "Last",
            "email": "newuser@example.com",  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
            "password1": "complexpass123",
            "password2": "complexpass123",
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert get_user_model().objects.filter(username="newuser").exists()

    # Test Update User
    # def test_user_update(self, client):
    #     user_model = get_user_model()
    #     user = user_model.objects.create_user(username="u1",
    #                                           password="pass123")  # NOSONAR
    #     client.login(username="u1", password="pass123")  # NOSONAR

    #     url = reverse("user_update", kwargs={"pk": user.id})
    #     response = client.post(
    #         url,
    #         {
    #             "username": "u1_updated",
    #             "first_name": "Name",
    #             "last_name": "Surname",
    #             "password1": "newpass12345",  # NOSONAR
    #             "password2": "newpass12345",  # NOSONAR
    #         },
    #     )
    #     assert response.status_code == 302
    #     user.refresh_from_db()
    #     assert user.username == "u1_updated"


    def test_user_update(self, client):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username="u1",
            password="pass123",
            email="u1@example.com"
        )
        client.login(username="u1", password="pass123")

        url = reverse("user_update", kwargs={"pk": user.id})
        response = client.post(
            url,
            {
                "username": "u1_updated",
                "first_name": "Name",
                "last_name": "Surname",
                "email": "u1_updated@example.com",
            },
        )
        
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.username == "u1_updated"
        assert user.first_name == "Name"
        assert user.last_name == "Surname"
        assert user.email == "u1_updated@example.com"

    # Test Delete User
    def test_user_delete(self, client):
        user_model = get_user_model()
        user = user_model.objects.create_user(username="u1",
                                              password="pass123")  # NOSONAR
        client.login(username="u1", password="pass123")  # NOSONAR

        url = reverse("user_delete", kwargs={"pk": user.id})
        response = client.post(url)
        assert response.status_code == 302
        assert not user_model.objects.filter(id=user.id).exists()

    # Test LogIn
    def test_login_logout(self, client):
        user_model = get_user_model()
        user_model.objects.create_user(username="u1",
                                       password="pass123")  # NOSONAR

        login_url = reverse("login")
        response = client.post(
            login_url,
            {"username": "u1", "password": "pass123"},  # NOSONAR
        )
        assert response.status_code == 302

        logout_url = reverse("logout")
        response = client.get(logout_url)
        assert response.status_code == 302


def test_get_extra_data():
    middleware = CustomRollbarNotifierMiddleware(dummy_get_response)
    request = types.SimpleNamespace()
    exc = Exception()

    data = middleware.get_extra_data(request, exc)
    assert "feature_flags" in data
    assert data["feature_flags"] == ["feature_1", "feature_2"]


@pytest.mark.django_db
def test_get_payload_data_authenticated_user():
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="pass",  # NOSONAR
        first_name="Test",
        last_name="User",
    )
    request = types.SimpleNamespace()
    request.user = user
    exc = Exception()

    middleware = CustomRollbarNotifierMiddleware(dummy_get_response)
    payload = middleware.get_payload_data(request, exc)

    assert "person" in payload
    assert payload["person"]["username"] == "testuser"


def test_get_payload_data_anonymous_user():
    request = types.SimpleNamespace()
    request.user = AnonymousUser()
    exc = Exception()

    middleware = CustomRollbarNotifierMiddleware(dummy_get_response)
    payload = middleware.get_payload_data(request, exc)
    assert payload == {}