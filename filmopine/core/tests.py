from django.test import TestCase
from .models import User
from .serializers import UserCreateSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

class UserModelTest(TestCase):
    """
    Test case for the User model.
    """

    def setUp(self):
        """
        Set up a sample user object for use in the tests.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="testuser@example.com",
            first_name="Test",
            last_name="User"
        )

    def test_user_creation(self):
        """
        Test that a User object is created with the correct attributes.
        """
        user = self.user
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

    def test_user_email_uniqueness(self):
        """
        Test that the email field is unique for the User model.
        """
        with self.assertRaises(Exception):
            User.objects.create_user(
                username="anotheruser",
                password="password123",
                email="testuser@example.com"  # Same email as the first user
            )


class UserSerializerTest(TestCase):
    """
    Test case for the User serializers.
    """

    def setUp(self):
        """
        Set up a sample user object for use in the tests.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="testuser@example.com",
            first_name="Test",
            last_name="User"
        )

    def test_user_create_serializer(self):
        """
        Test that the UserCreateSerializer correctly serializes user data.
        """
        serializer = UserCreateSerializer(instance=self.user)
        expected_data = {
            "id": self.user.id,
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
        self.assertEqual(serializer.data, expected_data)

    def test_user_serializer(self):
        """
        Test that the UserSerializer correctly serializes user data.
        """
        serializer = UserSerializer(instance=self.user)
        expected_data = {
            "id": self.user.id,
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
        self.assertEqual(serializer.data, expected_data)

    def test_user_create_serializer_validation(self):
        """
        Test that the UserCreateSerializer raises validation errors for required fields.
        """
        serializer = UserCreateSerializer(data={})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ApiHomeViewTest(TestCase):
    """
    Test case for the api_home view.
    """

    def setUp(self):
        """
        Set up the API client for testing.
        """
        self.client = APIClient()

    def test_api_home_view(self):
        """
        Test that the api_home view returns the expected response.
        """
        response = self.client.get('/api/')  # Adjust the URL as needed
        expected_data = {
            "name": "Film Opine API",
            "version": "1.0.0",
            "author": "Solomon Mokua Marita",
            "github repository": "https://github.com/solmarita/alx_capstone",
            "message": "Welcome to the Film Opine API, a Movie Review and Rating API developed for the ALX Back-End Web Development Capstone Project.",
            "swagger": "URL-PENDING"
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
