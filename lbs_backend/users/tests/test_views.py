from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import Gender


from users.tests.test_setup import TestSetup

User = get_user_model()

class TestViews(TestSetup):

    def test_user_registration_with_endpoints(self):
        gender_id = Gender.objects.get(id=1).id
        user = self.client.post(self.register_url, data={
            **self.user_b, 'LastName': "Kipyegon", "LocationID": 1, "GenderID": gender_id
        })
        self.assertEqual(201, user.status_code)
        self.assertEqual(2, user.data["id"])
    
    def test_user_registration_with_wrong_values(self):
        user_data = {**self.user_a}
        user_data.pop("IDNumber")
        user = self.client.post(self.register_url, data=user_data)
        self.assertEqual(400, user.status_code)