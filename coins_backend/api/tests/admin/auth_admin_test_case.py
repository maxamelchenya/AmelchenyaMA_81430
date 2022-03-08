from django.test import TestCase
from django.test import Client


class AuthAdminTestCase(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="testadmin@gmail.com", password="testadmin")