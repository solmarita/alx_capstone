from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta): #inherits everything in the Meta Class of the base class
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

# Replace Djoser's user serializer to redefine the fields it returns.
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        ref_name = 'CustomUser' # Setting unique reference name, it was confilicting with another serializer