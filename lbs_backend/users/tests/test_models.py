from django.contrib.auth import get_user_model
from .test_setup import TestSetup

from users.models import Gender

User = get_user_model()

class TestModels(TestSetup):
    
    def test_user_creation(self): # test user model creation
        user = User(**self.user_a)
        user.save()
        self.assertEqual(1, user.id)

    def test_user_details_update(self): # test user model updates
        gender = Gender(**self.gender)
        gender.save()
        self.assertEqual(1, gender.id)
        user = User(**self.user_a)
        user.save()
        self.assertEqual(1, user.id)
        user.GenderID = gender
        user.save()
        self.assertEqual(gender.id, user.GenderID_id)