from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.
class UserManagerTests(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            phone="+821012345678",
            user_type="Composer",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))
