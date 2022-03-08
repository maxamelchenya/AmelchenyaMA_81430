from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestSignUp(APITestCase):
    fixtures = ["fixtures.json"]
    url_name = "signup-list"

    def test_successful_sign_up(self):
        sign_up_data = {
            "username": "maxim",
            "email": "maxim@gmail.com",
            "password": "maximmaxim",
        }
        response = self.client.post(reverse(self.url_name), sign_up_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )

    def test_existing_email_sign_up(self):
        sign_up_data = {
            "username": "maxim",
            "email": "testuser1@gmail.com",
            "password": "maximmaxim",
        }
        response = self.client.post(reverse(self.url_name), sign_up_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )

    def test_missing_data_sign_up(self):
        sign_up_data = {}
        response = self.client.post(reverse(self.url_name), sign_up_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )
        self.assertEqual(len(response.data), 3)
