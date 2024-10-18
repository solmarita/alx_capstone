from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Review
from movie.models import Movie  # Import your Movie model

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    This serializer is used to validate and serialize Review instances, including additional fields
    for the movie title and the currently authenticated user.

    Attributes:
        movie_title (SerializerMethodField): The title of the movie associated with the review.
        user (HiddenField): The user who created the review, automatically set to the currently authenticated user.
    
    Meta:
        model (Review): The model that this serializer is based on.
        fields (list): A list of fields to be included in the serialized representation.
    """
        
    movie_title = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ['id', 'user', 'content_type', 'object_id', 'movie_title', 'review_title', 'review_content', 'rating', 'created_at', 'updated_at']
    
    def get_movie_title(self, obj):
            """
            Retrieve the title of the movie associated with the review.

            This method checks if the content type of the review corresponds to a movie.
            If so, it attempts to retrieve the movie instance using the object_id. If the movie exists,
            its title is returned; otherwise, None is returned.

            Args:
                obj (Review): The review instance for which the movie title is being retrieved.

            Returns:
                str or None: The title of the associated movie if it exists; otherwise, None.
            """
            # Get the ContentType instance for the object's content_type
            content_type = ContentType.objects.get(id=obj.content_type_id)  # Use content_type_id
            
            if content_type.model == 'movie':  # Check if the content type is 'movie'
                try:
                    movie = Movie.objects.get(id=obj.object_id)
                    return movie.title  # Return the movie title
                except Movie.DoesNotExist:
                    return None  # Handle case where the movie does not exist
            return None  # Return None if the content type is not 'movie'