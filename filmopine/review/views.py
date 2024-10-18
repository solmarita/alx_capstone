from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Review
from .serializers import ReviewSerializer
from movie.models import Movie
from core.permissions import IsAdminOrOwner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ReviewViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling reviews associated with movies.

    This viewset provides standard actions to create, retrieve, update, and delete reviews.
    Only admins and the owners of the review are allowed to modify or delete reviews.

    Attributes:
        queryset (QuerySet): A queryset of all Review objects.
        serializer_class (Serializer): The serializer class for validating and serializing Review data.
        permission_classes (list): A list of permission classes that restrict access based on user roles.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrOwner]

    def perform_create(self, serializer):
        """
        Save a new review instance, assigning the current authenticated user as the review's author.

        This method prevents user impersonation by ensuring that the `user` field of the review
        is automatically set to the currently authenticated user when a review is created.

        Args:
            serializer (ReviewSerializer): The serializer instance that contains the validated data for the review.
        """
                
        # Prevent user impersonation by setting the user field to the current authenticated user
        serializer.save(user=self.request.user)
    
class GenericReviewPagination(PageNumberPagination):
    """
    Custom pagination class for paginating review results.

    This pagination class is designed to limit the number of reviews returned in a single response,
    making it easier to manage large sets of review data. It provides options for clients to 
    customize the page size while enforcing a maximum limit to prevent excessively large requests.

    Attributes:
        page_size (int): The default number of reviews to display per page (set to 10).
        page_size_query_param (str): The name of the query parameter that clients can use to override the default page size.
        max_page_size (int): The maximum number of reviews that can be requested in a single page (set to 10).
    """

    page_size = 10  # Limit to 10 reviews per page
    page_size_query_param = 'page_size'  # Optional override
    max_page_size = 10  # Prevent large requests

class ReviewListAPIView(APIView):
    """
    API view to retrieve paginated reviews for a specific object based on its content type.

    This view allows clients to fetch reviews associated with a particular object, 
    such as a movie or series. It utilizes pagination to manage the number of reviews 
    returned in a single request, making it easier to handle large sets of review data.

    Methods:
        get(request, object_id, content_type='movie'):
            Handles GET requests to fetch reviews for a specified object.
            Accepts an `object_id` to identify the specific object and an optional `content_type` 
            parameter to determine the type of object (default is 'movie').

    Returns:
        Response: A paginated response containing the serialized reviews for the specified object,
                  or an error message if the content type is invalid.
    """
    pagination_class = GenericReviewPagination

    def get(self, request, object_id, content_type='movie'):
        """
        Retrieve paginated reviews for a specific object identified by its object ID and content type.

        This method handles GET requests to fetch reviews related to a specific object (e.g., 
        a movie or series). It checks if the specified content type is valid and then retrieves 
        the corresponding reviews. The results are paginated to manage the response size.

        Args:
            request: The HTTP request object.
            object_id (str): The ID of the object for which reviews are being requested.
            content_type (str): The type of the object (default is 'movie'). This is used to identify 
                                the content type in the database.

        Returns:
            Response: A paginated response containing serialized review data for the specified object.
                    If the content type is invalid, a 404 response with an error message is returned.
        """
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
        """
        Retrieve a specific review by its UUID and the associated object ID.

        This method handles GET requests to fetch a single review based on its unique identifier 
        (UUID) and the ID of the object (e.g., a movie) it is associated with. If the review is 
        not found, it returns a 404 error with an appropriate message.

        Args:
            request: The HTTP request object.
            object_id (str): The ID of the object to which the review belongs.
            review_id (str): The UUID of the review being requested.

        Returns:
            Response: A JSON response containing the serialized review data. If the review does 
                    not exist, a 404 response with an error message is returned.
        """
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
    
    # Define query parameters using swagger_auto_schema
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'movie_title', openapi.IN_QUERY,
                description="Filter reviews by movie title",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'rating', openapi.IN_QUERY,
                description="Filter reviews by rating (1.0 - 5.0)",
                type=openapi.TYPE_NUMBER,
                format='float'
            ),
        ],
        responses={200: "Paginated list of reviews"}
    )
    def get(self, request):
        """
        Search for reviews by movie title or rating.

        This method handles GET requests to filter and retrieve reviews based on specified query 
        parameters: movie title and/or rating. The results are paginated for easier consumption.

        Query Parameters:
            movie_title (str, optional): The title of the movie to filter reviews. The search 
                                        is case-insensitive and matches titles containing the 
                                        specified substring.
            rating (float, optional): The rating to filter reviews. Must be a float value between 
                                    1.0 and 5.0.

        Returns:
            Response: A paginated JSON response containing the serialized list of reviews that 
                    match the specified filters. If no reviews are found, an empty list is returned.
        """
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

class ReviewMeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = GenericReviewPagination

    def get(self, request):
        """
        Retrieve all reviews submitted by the currently authenticated user.

        This method handles GET requests to fetch and return a paginated list of reviews that 
        the authenticated user has submitted. If the user has no reviews, an empty list will be returned.

        Returns:
            Response: A paginated JSON response containing the serialized list of reviews 
                    submitted by the authenticated user. Each review includes relevant details 
                    such as title, content, rating, and timestamps.
        """
        user = request.user  # Get the currently authenticated user

        # Fetch reviews created by the current user
        reviews = Review.objects.filter(user=user)

        # Apply pagination
        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        # Serialize the reviews
        serializer = ReviewSerializer(paginated_reviews, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)