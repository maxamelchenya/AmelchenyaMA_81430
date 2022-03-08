from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .base_auth_api_test_case import BaseAuthAPITestCaseView


class TestCoinAdd(BaseAuthAPITestCaseView):
    url_name = "add-coin-list"

    def test_successful_coin_add(self):
        data = {
            "country": 1,
            "category": 1,
            "name": "Coin8",
            "description": "description",
            "year": 1933,
            "price": "5555.55",
        }
        response = self.client.post(reverse(self.url_name), data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )
        self.assertEqual(response.data["name"], data["name"])

    def test_no_auth_coin_add(self):
        self.client = APIClient()
        data = {
            "country": 1,
            "category": 1,
            "name": "Coin8",
            "description": "description",
            "year": 1933,
            "price": "5555.55",
        }
        response = self.client.post(reverse(self.url_name), data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
