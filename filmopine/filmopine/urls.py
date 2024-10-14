"""
URL configuration for filmopine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/api/', permanent=False)),  # Redirect root URL to /api/ (permanent: This parameter specifies whether the redirection is permanent (HTTP status 301) or temporary (HTTP status 302). Setting it to False means a temporary redirect.)
    path('api/', include('core.urls')), # Include core app URLs
    path('api/movies/', include('movie.urls')), # Include movies app URLs
    path('api/reviews/', include('review.urls')), # Include reviews app URLs
]
