from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from users.models import Gender

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
    
    def create_gender(self):
        gender = Gender(name="Male")
        gender.save()
        return gender
    
    def user_creation(self):
        user = User(**self.user_a)
        user.save()
        return user
    
    def user_registratin(self):
        res = self.client.post(self.register_url, self.user_a, format="json")
        return res
    
    def user_login(self):
        registration = self.user_registratin()
        login_data = {
            "password": self.user_a["password"], "MobileNumber": registration.data["MobileNumber"]
        }
        res = self.client.post(self.login_url, data=login_data)
        return res
    
    def tearDown(self):
        return super().tearDown()