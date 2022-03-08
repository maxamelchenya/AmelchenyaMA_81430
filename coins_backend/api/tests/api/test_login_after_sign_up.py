from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestLoginAfterSignUp(APITestCase):
    login_url_name = "login"
    signup_url_name = "signup-list"

    def test_login_after_sign_up(self):
        sign_up_data = {
            "username": "maxim",
            "email": "maxim@gmail.com",
            "password": "maximmaxim",
        }
        response = self.client.post(
            reverse(self.signup_url_name), sign_up_data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )
        sign_in_data = {
            "email": "maxim@gmail.com",
            "password": "maximmaxim",
        }
        response = self.client.post(
            reverse(self.login_url_name), sign_in_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertNotEqual(response.data["token"], "")
