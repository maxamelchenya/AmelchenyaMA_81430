from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .base_auth_api_test_case import BaseAuthAPITestCaseView


class TestCoinBid(BaseAuthAPITestCaseView):
    url_name = "bid-coin-detail"

    def test_successful_coin_bid(self):
        data = {"price": "12.00"}
        response = self.client.patch(
            reverse(self.url_name, kwargs={"pk": 1}), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data["price"], data["price"])

    def test_too_low_coin_bid(self):
        data = {"price": "0.01"}
        response = self.client.patch(
            reverse(self.url_name, kwargs={"pk": 1}), data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )

    def test_no_auth_coin_bid(self):
        self.client = APIClient()
        response = self.client.patch(
            reverse(self.url_name, kwargs={"pk": 1}), format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )
