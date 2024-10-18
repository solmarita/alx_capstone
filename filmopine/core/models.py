from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    This model overrides the default email field to ensure it is unique.
    This allows for better user identification and management within the application.

    Attributes:
        email (EmailField): A unique email address for the user, required for authentication and communication.

    Note:
        Ensure to update any relevant settings in your project to point to this custom user model.
    """
    email = models.EmailField(unique=True)