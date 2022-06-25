from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetup(APITestCase):
    
    def setUp(self):
        self.register_url = reverse("user")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

        self.user_a = {
            "IDNumber": 38598118, "FirstName": "Amos",
            "MobileNumber": "0794818111", "password": "amos2001"
        }
        self.gender = {
            "name": "Male"
        }

        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()