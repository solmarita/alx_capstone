import requests
from decouple import config
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieSearchView(APIView):
    OMDB_API_KEY = config('OMDB_API_KEY')
    OMDB_BASE_URL = 'http://www.omdbapi.com/'

    def get(self, request):
        query = request.query_params.get('query')

        # If no query is provided, return all movies
        if not query:
            # Optionally, you can return a message or a list of all movies
            movies = Movie.objects.all()
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=200)

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

        return Response(movies, status=200)