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

    def test_new_user_without_email_raises_error(self):
        """ Test thet creating a user without an email raises a ValueError """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """ Test creating a superuser. """
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'testpas123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
