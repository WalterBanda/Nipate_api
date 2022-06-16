from rest_framework import status
from .test_setup import TestSetup
from users.models import Gender
from django.contrib.auth import get_user_model

User = get_user_model()

class TestViews(TestSetup):

    def test_user_can_register(self):
        res = self.client.post(self.register_url, self.user_a, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, res.data["id"])
    
    def test_user_details_update(self):
        gender = Gender(name="Male")
        gender.save()
        self.assertEqual(1, gender.id)
        user_a = User(**self.user_a)
        user_a.GenderID = gender
        user_a.save()
        self.assertEqual(1, user_a.id)

    def test_user_login(self):
        response = self.client.post(self.register_url, self.user_a, format="json")
        login_data = {
            "password": self.user_a["password"],
            "MobileNumber": response.data["MobileNumber"]
        }
        res = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        response = self.client.post(self.register_url, self.user_a, format="json")
        login_data = {
            "password": self.user_a["password"],
            "MobileNumber": response.data["MobileNumber"]
        }
        res = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        auth_token = res.data["auth_token"]
        logout_res = self.client.post(self.logout_url, header={"Authorization": "Token\1" + auth_token})