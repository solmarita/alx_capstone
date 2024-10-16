from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.contenttypes.models import ContentType
from .models import Review
from .serializers import ReviewSerializer
from movie.models import Movie

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
class GenericReviewPagination(PageNumberPagination):
    page_size = 10  # Limit to 10 reviews per page
    page_size_query_param = 'page_size'  # Optional override
    max_page_size = 10  # Prevent large requests

class ReviewListAPIView(APIView):
    pagination_class = GenericReviewPagination

    def get(self, request, object_id, content_type='movie'):
        """Fetch reviews for a specific object via content type."""
        try:
            content_type_obj = ContentType.objects.get(app_label=content_type, model=content_type)
        except ContentType.DoesNotExist:
            return Response({"detail": "Invalid content type."}, status=404)

        # Filter reviews related to the specific object
        reviews = Review.objects.filter(content_type=content_type_obj, object_id=object_id)

        # Apply pagination
        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        # Serialize the reviews
        serializer = ReviewSerializer(paginated_reviews, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
    
class ReviewDetailAPIView(APIView):
    def get(self, request, object_id, review_id):
        """Retrieve a specific review by UUID."""
        try:
            # Fetch the review using the UUID and object_id
            review = Review.objects.get(id=review_id, object_id=object_id)
        except Review.DoesNotExist:
            return Response({"detail": "Review not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the review
        serializer = ReviewSerializer(review)

        return Response(serializer.data)
    
class ReviewSearchAPIView(APIView):
    pagination_class = GenericReviewPagination

    def get(self, request):
        """Search for reviews by movie title or rating."""
        movie_title = request.query_params.get('movie_title')
        rating = request.query_params.get('rating')

        # Build the query filters
        filters = Q()

        if movie_title:
            # Find content types associated with Movie
            content_type_movie = ContentType.objects.get(app_label='movie', model='movie')

            # Get movie IDs that match the title
            movies = Movie.objects.filter(title__icontains=movie_title)
            movie_ids = movies.values_list('id', flat=True)

            # Add to filters
            filters &= Q(content_type=content_type_movie, object_id__in=movie_ids)

        if rating:
            # Filter by rating
            filters &= Q(rating=rating)

        # Fetch reviews based on the filters
        reviews = Review.objects.filter(filters)

        # Apply pagination
        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        # Serialize the reviews
        serializer = ReviewSerializer(paginated_reviews, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)