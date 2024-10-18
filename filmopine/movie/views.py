import requests
from decouple import config
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from core.permissions import IsAdminOrReadOnly
from .models import Movie
from .serializers import MovieSerializer

class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Movie model in the Film Opine API.

    This viewset provides the standard actions for CRUD operations (Create, Read, Update, Delete)
    on Movie instances. It uses the MovieSerializer for serialization and deserialization of data.
    The viewset also enforces custom permissions to restrict access to certain actions.

    Attributes:
        queryset (QuerySet): The set of all Movie instances to be queried.
        serializer_class (MovieSerializer): The serializer used to validate and serialize data.
        permission_classes (list): A list of permission classes that determine access rights;
            only admins can perform create, update, and delete actions, while read operations
            are allowed for all users.

    Methods:
        list(request): Retrieves a paginated list of movies.
        create(request): Allows an admin to create a new movie.
        retrieve(request, pk): Retrieves details of a specific movie by its primary key (pk).
        update(request, pk): Allows an admin to update an existing movie.
        partial_update(request, pk): Allows an admin to partially update an existing movie.
        destroy(request, pk): Allows an admin to delete a specific movie by its primary key (pk).
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly] # custom permission

class MovieSearchPagination(PageNumberPagination):
    """
    Custom pagination class for movie search results in the Film Opine API.

    This pagination class defines the behavior for paginating movie search results.
    It allows clients to specify the number of items per page and imposes a maximum
    limit on the page size to prevent excessively large responses.

    Attributes:
        page_size (int): The default number of items to display per page, set to 10.
        page_size_query_param (str): The query parameter that clients can use to specify
            their desired page size.
        max_page_size (int): The maximum limit for the number of items per page, set to 100.

    Methods:
        paginate_queryset(queryset, request, view=None): 
            Paginates the given queryset based on the request parameters and returns
            a page of results.
    """
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size
    max_page_size = 100  # Maximum limit for page size

class MovieSearchView(APIView):
    """
    API View for searching movies using the OMDb API and retrieving local movie data.

    This view handles GET requests to search for movies based on a query parameter.
    If no query is provided, it returns all movies in the local database with pagination.
    When a query is given, it fetches matching movies from the OMDb API, updates or
    creates corresponding entries in the local database, and returns the results with
    pagination.

    Attributes:
        OMDB_API_KEY (str): The API key for accessing the OMDb API.
        OMDB_BASE_URL (str): The base URL for the OMDb API.
        paginator (MovieSearchPagination): The custom pagination class for movie search results.

    Methods:
        get(request):
            Handles GET requests to search for movies and return results.
            If a query is provided, it fetches data from the OMDb API; otherwise,
            it returns all movies from the local database.
    """
    OMDB_API_KEY = config('OMDB_API_KEY')
    OMDB_BASE_URL = 'http://www.omdbapi.com/'
    paginator = MovieSearchPagination()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, 
                              description="Search term for movies", type=openapi.TYPE_STRING),
        ],
        responses={
            200: "Paginated list of movies",
            404: "Movie not found"
        }
    )
    def get(self, request):
        """
        Handles GET requests for searching movies.

        This method retrieves movies based on a search query provided as a query parameter.
        If no query is provided, it returns all movies from the local database with pagination.
        If a query is provided, it fetches matching movies from the OMDb API, updates or creates
        corresponding entries in the local database, and returns the results with pagination.

        Args:
            request (Request): The HTTP request object containing query parameters.

        Returns:
            Response: A paginated response containing either:
                - A list of all movies if no query is provided.
                - A list of movies matching the query from the OMDb API, 
                along with the status code indicating success or failure.
        """
        query = request.query_params.get('query')

        # If no query is provided, return all movies
        if not query:
            # Retrieve all movies and paginate
            movies = Movie.objects.all()
            paginated_movies = self.paginator.paginate_queryset(movies, request)

            serializer = MovieSerializer(paginated_movies, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        # Send a request to the OMDb API
        url = f"{self.OMDB_BASE_URL}?apikey={self.OMDB_API_KEY}&s={query}"
        omdb_response = requests.get(url).json()

        if omdb_response.get("Response") == "False":
            return Response({"error": omdb_response.get("Error")}, status=404)

        # Process each movie result
        movies = []
        for item in omdb_response.get("Search", []):
            imdb_id = item.get("imdbID")
            title = item.get("Title")
            year = item.get("Year")
            film_type = item.get("Type")
            poster = item.get("Poster")

            # Create or update the movie in the local DB
            movie, created = Movie.objects.update_or_create(
                imdb_id=imdb_id,
                defaults={
                    "title": title,
                    "year": year,
                    "film_type": film_type,
                    "poster": poster
                }
            )

            # Serialize the movie to include its local object ID
            serializer = MovieSerializer(movie)
            movies.append(serializer.data)

        # Paginate the results
        paginated_movies = self.paginator.paginate_queryset(movies, request)

        return self.paginator.get_paginated_response(paginated_movies)