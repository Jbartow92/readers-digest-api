from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Fields to include in the serialized representation of the User model
        fields = ['id', 'username', 'password']
        # Specify that the 'password' field should be write-only
        extra_kwargs = {'password': {'write_only': True}}

# ViewSet for handling User-related operations
class UserViewSet(viewsets.ViewSet):
    # Queryset containing all User objects
    queryset = User.objects.all()
    # Set permission classes to allow any user
    permission_classes = [permissions.AllowAny]

    # Custom action to register a new user
    @action(detail=False, methods=['post'], url_path='register')
    def register_account(self, request):
        # Serialize the incoming data
        serializer = UserSerializer(data=request.data)
        # Check if the data is valid
        if serializer.is_valid():
            # Create a new user
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            # Generate or retrieve an authentication token for the user
            token, created = Token.objects.get_or_create(user=user)
            # Return the token in the response
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        # Return errors if data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom action to handle user login
    @action(detail=False, methods=['post'], url_path='login')
    def user_login(self, request):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        # Check if authentication is successful
        if user:
            # Retrieve or generate a token for the authenticated user
            token = Token.objects.get(user=user)
            # Return the token in the response
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            # Return an error response for invalid credentials
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
