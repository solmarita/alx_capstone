from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_home(request):
    data = {
        "name": "Film Opine API",
        "version": "1.0.0",
        "author": "Solomon Mokua Marita",
        "github repository": "https://github.com/solmarita/alx_capstone",
        "message": "Welcome to the Film Opine API, a Movie Review and Rating API developed for the ALX Back-End Web Development Capstone Project.",
        "swagger": "URL-PENDING"
    }
    return Response(data)
