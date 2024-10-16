from django.db import models

# Create your models here.
class Movie(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    year = models.CharField(max_length=10, blank=True, null=True)  # Store as string since years can vary
    film_type = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'movie', 'series'
    poster = models.URLField(max_length=500, blank=True, null=True)  # Allow URLs


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title