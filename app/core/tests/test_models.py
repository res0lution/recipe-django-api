from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.
class ModelTests(TestCase):
    def test_create_user_with_email_successfull(self):
        """Test creating a new user with an email is successful"""
        email = "test@email.com"
        password = "usertestpassword123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@EMAIL.com"
        password = "usertestpassword123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_email_invalid_email(self):
        """Test creating user with no email raises error"""
        password = "usertestpassword123"
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password=password
            )

    def test_create_superuser(self):
        """Test creating a new superuser"""
        email = "test@email.com"
        password = "usertestpassword123"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
