from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .base_auth_api_test_case import BaseAuthAPITestCaseView


class TestUsersCoinsList(BaseAuthAPITestCaseView):
    url_name = "users-coins-list"

    def test_get_users_coins(self):
        response = self.client.get(reverse(self.url_name), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 5)

    def test_no_auth_get_users_coins(self):
        self.client = APIClient()
        response = self.client.get(reverse(self.url_name), format="json")
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
