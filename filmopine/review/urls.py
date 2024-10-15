from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, ReviewListAPIView

router = DefaultRouter()
router.register('', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include all review routes
]