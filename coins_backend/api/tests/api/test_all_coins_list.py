from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestAllCoinsList(APITestCase):
    fixtures = ["fixtures.json"]
    url_name = "all-coins-list"

    def test_get_coins(self):
        response = self.client.get(reverse(self.url_name), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 7)

    def test_get_coins_ordered_by_name_acs(self):
        response = self.client.get(
            reverse(self.url_name), {"ordering": "name"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data[0]["id"], 1)

    def test_get_coins_ordered_by_name_desc(self):
        response = self.client.get(
            reverse(self.url_name), {"ordering": "-name"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data[0]["id"], 7)

    def test_get_coins_ordered_by_year_acs(self):
        response = self.client.get(
            reverse(self.url_name), {"ordering": "year"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data[0]["id"], 2)

    def test_get_coins_ordered_by_year_desc(self):
        response = self.client.get(
            reverse(self.url_name), {"ordering": "-year"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data[0]["id"], 5)

    def test_get_coins_filtered_by_category_name(self):
        response = self.client.get(
            reverse(self.url_name), {"category__name": "Unusual"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 2)
        coin_id_list = [coin["id"] for coin in response.data]
        self.assertEqual(coin_id_list, [6, 7])

    def test_get_coins_filtered_by_country_name(self):
        response = self.client.get(
            reverse(self.url_name), {"country__name": "Russia"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], 5)

    def test_get_coins_filtered_by_min_price_and_max_price(self):
        response = self.client.get(
            reverse(self.url_name),
            {"min_price": "1.00", "max_price": "5555.00"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 5)
        coin_id_list = [coin["id"] for coin in response.data]
        self.assertEqual(coin_id_list, [1, 2, 3, 4, 6])

    def test_get_coins_filtered_by_min_price(self):
        response = self.client.get(
            reverse(self.url_name), {"min_price": "1.00"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 6)
        coin_id_list = [coin["id"] for coin in response.data]
        self.assertEqual(coin_id_list, [1, 2, 3, 4, 6, 7])

    def test_get_coins_filtered_by_max_price(self):
        response = self.client.get(
            reverse(self.url_name), {"max_price": "5555.00"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 6)
        coin_id_list = [coin["id"] for coin in response.data]
        self.assertEqual(coin_id_list, [1, 2, 3, 4, 5, 6])
