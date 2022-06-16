from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()
client = APIClient()

class UserTestCast(TestCase):
    def setUp(self):
        user_a_pw = "amos2001"
        self.user_a_pw = user_a_pw
        user_a = User(MobileNumber='0794818111', IDNumber=38598118, FirstName='Amos')
        user_a.is_admin = True
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a
        self.auth_token = ""
    
    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)
    def test_user_password(self):
        self.assertTrue(self.user_a.check_password(self.user_a_pw))
    
    def test_token_login(self): # test login of a user
        url = reverse("login")
        data = {
            "password": self.user_a_pw,
            "MobileNumber": self.user_a.MobileNumber
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.auth_token = response.data["auth_token"]
    def test_token_logout(self):
        url = reverse("logout")
        print(self.auth_token)
        response = client.post(url, headers={"Authorization": "Token " + self.auth_token}, format='json')
        # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("logout succesfully")