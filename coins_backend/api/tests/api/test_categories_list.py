from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestCategoriesList(APITestCase):
    fixtures = ["fixtures.json"]
    url_name = "categories-list"

    def test_get_categories(self):
        response = self.client.get(reverse(self.url_name), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.data), 8)
