from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.
class UserManagerTests(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(
            email="test@example.com",
            username="testuser",
            phone="+821012345678",
            password="password123",
            user_type="Composer",
        )
        print(f"생성된 유저: {user}")

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))

    def test_password_hashing(self):
        user = self.User.objects.create_user(
            email="test@example.com",
            username="testuser",
            phone="+821012345678",
            password="password123",
            user_type="Composer",
        )
        self.assertNotEqual("password123", user.password)

