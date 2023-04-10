from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from lawadvisor.utils import get_error_message
# Create your views here.


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        serializer.save()
        return Response({'message': 'Registration successful'}, status=status.HTTP_200_OK)
    else:

        return Response({'error':  get_error_message(serializer)}, status=status.HTTP_400_BAD_REQUEST)
