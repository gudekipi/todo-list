from django.contrib.auth import authenticate
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .serializers import LoginSerializer, LogoutSerializer
# Create your views here.


@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK )
    return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    serializer = LogoutSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
