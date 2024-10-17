from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Review
from movie.models import Movie  # Import your Movie model

class ReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'content_type', 'object_id', 'movie_title', 'review_title', 'review_content', 'rating', 'created_at', 'updated_at']
    
    def get_movie_title(self, obj):
            # Get the ContentType instance for the object's content_type
            content_type = ContentType.objects.get(id=obj.content_type_id)  # Use content_type_id
            
            if content_type.model == 'movie':  # Check if the content type is 'movie'
                try:
                    movie = Movie.objects.get(id=obj.object_id)
                    return movie.title  # Return the movie title
                except Movie.DoesNotExist:
                    return None  # Handle case where the movie does not exist
            return None  # Return None if the content type is not 'movie'