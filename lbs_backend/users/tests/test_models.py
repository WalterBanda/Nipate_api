from rest_framework import status
from .test_setup import TestSetup

class TestModels(TestSetup):
    
    def test_user_creation(self): # test user model creation
        user = self.user_creation()
        self.assertEqual(1, user.id)

    def test_user_details_update(self): # test user model updates
        gender = self.create_gender()
        self.assertEqual(1, gender.id)
        user = self.user_creation()
        self.assertEqual(1, user.id)
        user.GenderID = gender
        user.save()
        self.assertEqual(gender.id, user.GenderID_id)