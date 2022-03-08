from django.urls import reverse
from rest_framework import status
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from api.models import Coin

from .auth_admin_test_case import AuthAdminTestCase


class TestCoinsAdmin(AuthAdminTestCase):

    def test_coins_changelist(self):
        response = self.client.get(
            reverse(admin_urlname(Coin._meta, "changelist")), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_coin_change(self):
        response = self.client.get(reverse(admin_urlname(Coin._meta, "change"), args=[1]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_coin_delete(self):
        response = self.client.get(reverse(admin_urlname(Coin._meta, "delete"), args=[1]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)