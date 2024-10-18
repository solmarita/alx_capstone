from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.test import APIRequestFactory
from .models import Review
from movie.models import Movie  # Make sure to import your Movie model
from .serializers import *
import uuid

User = get_user_model()

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            # other required fields for Movie
        )
        self.review = Review.objects.create(
            user=self.user,
            content_type=ContentType.objects.get_for_model(self.movie),
            object_id=self.movie.id,
            review_title='Great Movie',
            review_content='This movie was amazing!',
            rating=4.5
        )

    def test_review_creation(self):
        self.assertEqual(self.review.review_title, 'Great Movie')
        self.assertEqual(self.review.rating, 4.5)
        self.assertEqual(self.review.user, self.user)

    def test_review_str(self):
        self.assertEqual(str(self.review), 'Great Movie - 4.5/5')


class ReviewSerializerTest(TestCase):
    def setUp(self):
        # Create a user and a movie for testing
        self.user = User.objects.create_user(username='testuser', password='password')
        self.movie = Movie.objects.create(title='Test Movie')

        # Example review data
        self.review_data = {
            'user': self.user.id,
            'content_type': ContentType.objects.get_for_model(Movie).id,
            'object_id': self.movie.id,
            'review_title': 'Great Movie',
            'review_content': 'I really enjoyed this movie!',
            'rating': 4.5,
        }

        # Create a request factory
        self.factory = APIRequestFactory()

    def test_review_serializer(self):
        request = self.factory.post('/fake-url/', {})
        request.user = self.user  # Set the user for the request

        serializer = ReviewSerializer(data=self.review_data, context={'request': request})
        self.assertTrue(serializer.is_valid())

    def test_invalid_rating(self):
        invalid_data = self.review_data.copy()
        invalid_data['rating'] = 6.0  # Invalid rating
        request = self.factory.post('/fake-url/', {})
        request.user = self.user  # Set the user for the request

        serializer = ReviewSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('rating', serializer.errors)


class ReviewAPITest(APITestCase):
    def setUp(self):
        # Create a user and a movie for testing
        self.user = User.objects.create_user(username='testuser', password='password')
        self.movie = Movie.objects.create(title='Test Movie')

        # Get the ContentType for the Movie model
        self.content_type = ContentType.objects.get_for_model(Movie)

        # Example review data
        self.review_data = {
            'user': self.user,  # Assign the User instance
            'content_type': self.content_type,  # Assign the ContentType instance
            'object_id': self.movie.id,
            'review_title': 'Great Movie',
            'review_content': 'I really enjoyed this movie!',
            'rating': 4.5,
        }

        # Create a review for updating
        self.review = Review.objects.create(**self.review_data)

    def test_update_review(self):
        update_data = {'rating': 5.0}  # Assume we're just updating the rating
        url = reverse('review-detail', kwargs={'pk': self.review.id})  # Adjust the URL as needed
        self.client.force_authenticate(user=self.user)  # Authenticate the user

        response = self.client.patch(url, update_data, format='json')

        # Print the response data to debug
        print(response.data)  # This will show what went wrong

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 5.0)  # Check that the rating was updated