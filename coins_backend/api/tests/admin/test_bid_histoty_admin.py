from django.urls import reverse
from rest_framework import status
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from api.models import BidHistory

from .auth_admin_test_case import AuthAdminTestCase


class TestBidHistoryAdmin(AuthAdminTestCase):

    def test_did_history_changelist(self):
        response = self.client.get(
            reverse(admin_urlname(BidHistory._meta, "changelist")), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_bid_history_change(self):
        response = self.client.get(reverse(admin_urlname(BidHistory._meta, "change"), args=[1]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)