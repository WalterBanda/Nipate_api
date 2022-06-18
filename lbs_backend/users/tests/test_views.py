from rest_framework import status
from rest_framework.test import APIClient
from .test_setup import TestSetup


client = APIClient()

class TestViews(TestSetup):

    def test_user_can_register(self): # test user registration endpoint
        res = self.user_registratin()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, res.data["id"])
    
    def test_user_login(self): # test user login and authentication header token
        res = self.user_login()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_logout(self): # test user logout and deletion of authentication header token
        response = self.user_login()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        auth_token = response.data["auth_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token\s" + auth_token)
        logout_res = self.client.post(self.logout_url)