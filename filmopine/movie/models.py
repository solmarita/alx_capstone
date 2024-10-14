from django.db import models

# Create your models here.
class Movie(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title