from rest_framework import status
from .test_setup import TestSetup

class TestViews(TestSetup):

    def test_user_can_register(self): # test user registration endpoint
        res = self.user_registratin()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, res.data["id"])
    
    def test_user_login(self): # test user login and authentication header token
        res = self.user_login()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_logout(self): # test user logout and deletion of authentication header token
        response = self.client.post(self.register_url, self.user_a, format="json")
        login_data = {
            "password": self.user_a["password"],
            "MobileNumber": response.data["MobileNumber"]
        }
        res = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        auth_token = res.data["auth_token"]
        logout_res = self.client.post(self.logout_url, header={"Authorization": "Token\1" + auth_token})