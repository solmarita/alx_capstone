from django.db import models
from django.contrib.auth.models import AbstractUser

# Extending AbstractUser to make the email field unique, which it isn't out of the box
class User(AbstractUser):
    email = models.EmailField(unique=True)