from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Movie
from review.models import Review

class MovieSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'imdb_id', 'title', 'created_at', 'updated_at', 'reviews_count']

    def get_reviews_count(self, obj):
        content_type = ContentType.objects.get_for_model(Movie)
        return Review.objects.filter(content_type=content_type, object_id=obj.id).count()