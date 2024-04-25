"""
Tests for models
"""

from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_narmalized(self):
        """Test email is normalized for the new user"""
        sample_emails = [
            ["test1@Example.com", "test1@example.com"],
            ["test2@EXAMPLE.com", "test2@example.com"],
            ["test3@Example.COM", "test3@example.com"],
            ["teSt1@ExampLE.com", "teSt1@example.com"],
            ["test1@example.nl", "test1@example.nl"],
            ["test4@examPle.nl", "test4@example.nl"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test thet creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "testpas123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "testpass123",
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe name",
            # time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description.",
        )

        # self.assertContains(recipe, recipe.price)
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name="Tag1")

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingriedient is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(user=user, name="spinage")

        self.assertEqual(str(ingredient), ingredient.name)

    @patch("core.models.uuid.uuid4")
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, "example.jpg")

        self.assertEqual(file_path, f"uploads/recipe/{uuid}.jpg")
