"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """ Test models. """

    def test_create_user_with_email_successful(self):
        """ Test creating a user with an email is successful. """
        email = "test@example.com"
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_narmalized(self):
        """ Test email is normalized for the new user """
        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['test2@EXAMPLE.com', 'test2@example.com'],
            ['test3@Example.COM', 'test3@example.com'],
            ['teSt1@ExampLE.com', 'teSt1@example.com'],
            ['test1@example.nl', 'test1@example.nl'],
            ['test4@examPle.nl', 'test4@example.nl'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
