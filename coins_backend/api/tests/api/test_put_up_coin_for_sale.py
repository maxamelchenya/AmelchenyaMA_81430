from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ...models import Coin
from .base_auth_api_test_case import BaseAuthAPITestCaseView


class TestPutUpCoinForSaleList(BaseAuthAPITestCaseView):
    url_name = "users-coins-put-up-for-sale"

    def test_get_put_up_coin_success(self):
        response = self.client.post(
            reverse(self.url_name, kwargs={"pk": 8}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data["status"], Coin.STATUS_CHOICES[1][0])

    def test_get_put_up_another_users_coin(self):
        response = self.client.post(
            reverse(self.url_name, kwargs={"pk": 7}), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_no_auth_put_up_coin(self):
        self.client = APIClient()
        response = self.client.post(
            reverse(self.url_name, kwargs={"pk": 8}), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
