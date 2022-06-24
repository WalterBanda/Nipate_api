# from rest_framework import status
# from rest_framework.test import APIClient
# from .test_setup import TestSetup


# client = APIClient()

# class TestViews(TestSetup):


#     def test_user_login(self): # test user login and authentication header token
#         res = self.client.post(self.register_url, data=self.user_a)
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(1, res.data["id"])
#         user = {**self.user_a}
#         user.pop("IDNumber")
#         user.pop("FirstName")
#         login = self.client.post(self.login_url, data=user)
#         self.assertEqual(login.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(login.data)