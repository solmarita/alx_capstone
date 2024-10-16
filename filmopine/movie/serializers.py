from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from rest_framework import serializers
from .models import Movie
from review.models import Review

class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model in the Film Opine API.

    This serializer provides the structure for movie data, including additional fields
    for the number of reviews and the average rating. It is used to convert Movie
    instances into JSON format and vice versa.

    Attributes:
        reviews_count (int): The number of reviews associated with the movie.
        average_rating (float): The average rating of the movie based on reviews.

    Meta:
        model (Movie): The model associated with this serializer.
        fields (list): A list of fields to be included in the serialized representation,
            including 'id', 'imdb_id', 'title', 'year', 'film_type', 'poster',
            'reviews_count', 'average_rating', 'created_at', and 'updated_at'.
    """
    
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'imdb_id', 'title', 'year', 'film_type', 'poster', 'reviews_count', 'average_rating','created_at', 'updated_at']

    def get_reviews_count(self, obj):
        content_type = ContentType.objects.get_for_model(Movie)
        return Review.objects.filter(content_type=content_type, object_id=obj.id).count()
    
    def get_average_rating(self, obj):
        content_type = ContentType.objects.get_for_model(Movie)
        average = Review.objects.filter(content_type=content_type, object_id=obj.id).aggregate(Avg('rating'))['rating__avg']
        return average if average is not None else 0  # Return 0 if there are no reviews