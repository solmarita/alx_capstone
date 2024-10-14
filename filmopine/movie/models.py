from django.db import models

# Create your models here.
class Movie(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True)