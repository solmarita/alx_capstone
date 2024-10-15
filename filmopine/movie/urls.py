from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet
from review.views import ReviewListAPIView, ReviewDetailAPIView

router = DefaultRouter()
router.register('', MovieViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include all movie routes
    # path('<int:movie_id>/reviews/', MovieReviewsAPIView.as_view(), name='movie_reviews_api'),
    path('<int:object_id>/reviews/', ReviewListAPIView.as_view(), name='movie_reviews'),
    path('<int:object_id>/reviews/<uuid:review_id>/', ReviewDetailAPIView.as_view(), name='movie_review_detail'),  # New detail route within the movie app
]