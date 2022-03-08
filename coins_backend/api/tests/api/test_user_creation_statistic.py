from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class TestUserCreationStatistic(APITestCase):
    fixtures = ["fixtures.json"]
    url_name = "user-creation-statistic-list"
    login_url_name = "login"

    def setUp(self):
        sign_in_data = {"email": "testadmin@gmail.com", "password": "testadmin"}
        response = self.client.post(
            reverse(self.login_url_name), sign_in_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        auth_token = response.data["token"]
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + auth_token)

    def test_user_creation_statistic(self):
        response = self.client.get(reverse(self.url_name), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 6)
