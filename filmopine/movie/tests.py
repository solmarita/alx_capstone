from rest_framework.exceptions import ValidationError
from movie.serializers import MovieSerializer
from django.test import TestCase
from movie.models import Movie

class MovieSerializerTest(TestCase):
    """
    Test case for the MovieSerializer.
    """

    def setUp(self):
        """
        Set up a sample movie object for use in the tests.
        """
        self.movie = Movie.objects.create(
            imdb_id="tt4196776",
            title="Jason Bourne",
            year="2016",
            film_type="movie",
            poster="https://m.media-amazon.com/images/M/MV5BMzY3Y2Q3MmUtZmU3MC00OWMxLWIwNDMtNDA4MmViMTUxYjYxXkEyXkFqcGc@._V1_SX300.jpg"
        )

    def test_valid_movie_serializer(self):
        """
        Test that the serializer correctly validates valid data.
        """
        data = {
            "imdb_id": "tt1234567",
            "title": "Inception",
            "year": "2010",
            "film_type": "movie"
        }
        serializer = MovieSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_movie_serializer(self):
        """
        Test that the serializer raises a validation error for invalid data.
        """
        data = {"imdb_id": "", "title": ""}
        serializer = MovieSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('imdb_id', serializer.errors)
        self.assertIn('title', serializer.errors)

    def test_serializer_output(self):
        """
        Test that the serializer returns the core fields for a movie instance.
        """
        serializer = MovieSerializer(instance=self.movie)
        expected_data = {
            "id": self.movie.id,
            "imdb_id": "tt4196776",
            "title": "Jason Bourne",
            "year": "2016",
            "film_type": "movie",
            "poster": self.movie.poster,
        }
        for key, value in expected_data.items():
            self.assertEqual(serializer.data[key], value)



