from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'content_type', 'object_id', 'review_title', 'review_content', 'rating', 'created_at', 'updated_at']