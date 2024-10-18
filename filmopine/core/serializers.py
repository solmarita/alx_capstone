from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Serializer for creating new users, extending the functionality of the 
    BaseUserCreateSerializer.

    This serializer inherits from BaseUserCreateSerializer and includes the 
    following fields:
        - id: The unique identifier for the user.
        - username: The username for the user.
        - password: The user's password (hashed).
        - email: The user's email address (must be unique).
        - first_name: The user's first name.
        - last_name: The user's last name.

    It is used to validate and serialize user creation requests, ensuring that 
    the required fields are present and formatted correctly.

    Attributes:
        Meta: A nested class that defines the fields to be included in the 
              serialization process.

    Methods:
        None

    Returns:
        None
    """
    class Meta(BaseUserCreateSerializer.Meta): #inherits everything in the Meta Class of the base class
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

# Replace Djoser's user serializer to redefine the fields it returns.
class UserSerializer(BaseUserSerializer):
    """
    Serializer for representing user details, extending the functionality of 
    the BaseUserSerializer.

    This serializer inherits from BaseUserSerializer and includes the 
    following fields:
        - id: The unique identifier for the user.
        - username: The username of the user.
        - email: The email address of the user.
        - first_name: The user's first name.
        - last_name: The user's last name.

    It is used to serialize user instances for responses, ensuring that only 
    the specified fields are included in the output. A unique reference name 
    is set to avoid conflicts with other serializers.

    Attributes:
        Meta: A nested class that defines the fields to be included in the 
              serialization process and specifies a unique reference name.

    Methods:
        None

    Returns:
        None
    """
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        ref_name = 'CustomUser' # Setting unique reference name, it was confilicting with another serializer