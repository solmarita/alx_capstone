from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_home(request):
    """
    API Home view that provides basic information about the Film Opine API.

    This view responds to GET requests with a JSON object containing the 
    following details about the API:
        - name: The name of the API.
        - version: The current version of the API.
        - author: The author of the API.
        - github repository: URL to the API's GitHub repository.
        - message: A welcome message providing a brief description of the API's purpose.
        - swagger: URL for the API documentation (to be provided).

    Returns:
        Response: A JSON response containing the API information.

    Example response:
        {
            "name": "Film Opine API",
            "version": "1.0.0",
            "author": "Solomon Mokua Marita",
            "github repository": "https://github.com/solmarita/alx_capstone",
            "message": "Welcome to the Film Opine API, a Movie Review and Rating API developed for the ALX Back-End Web Development Capstone Project.",
            "swagger": "URL-PENDING"
        }
    """
    data = {
        "name": "Film Opine API",
        "version": "1.0.0",
        "author": "Solomon Mokua Marita",
        "github repository": "https://github.com/solmarita/alx_capstone",
        "message": "Welcome to the Film Opine API, a Movie Review and Rating API developed for the ALX Back-End Web Development Capstone Project.",
        "swagger": "URL-PENDING"
    }
    return Response(data)
