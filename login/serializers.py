from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer): 
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError()

class LogoutSerializer(serializers.Serializer):
    pass