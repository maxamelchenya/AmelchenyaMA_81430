import pytest
from django.test import Client
from api.models import User


@pytest.mark.django_db
class TestAdminLogin:
    def test_login(self):
        self.client = Client()
        my_admin = User(username="user", email="user@email.com")
        my_admin.set_password("passphrase")
        my_admin.is_superuser = True
        my_admin.is_staff = True
        my_admin.save()
        response = self.client.get("/admin/", follow=True)
        assert response.status_code == 200
        login_response = self.client.login(
            email="user@email.com", password="passphrase"
        )
        assert login_response==True
