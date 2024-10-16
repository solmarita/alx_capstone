from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, ReviewSearchAPIView, ReviewMeAPIView

router = DefaultRouter()
router.register('', ReviewViewSet)

urlpatterns = [
    path('search/', ReviewSearchAPIView.as_view(), name='review-search'),
    path('me/', ReviewMeAPIView.as_view(), name='review-me'),
    path('', include(router.urls)),  # Include all review routes
]