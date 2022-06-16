from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class TestSetup(APITestCase):
    
    def setUp(self):
        self.register_url = "http://127.0.0.1:8000/auth/register/"
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

        self.user_a = {
            "IDNumber": 38598118,
            "FirstName": "Amos",
            "MobileNumber": "0794818111",
            "password": "amos2001"
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()