from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import ConfirmationCode


class RegistrationSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_active=False  
        )
        code_obj = ConfirmationCode.objects.create(user=user)
        code_obj.generate_code()
        return user


class ConfirmationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)
    
    def validate_code(self, value):
        try:
            ConfirmationCode.objects.get(code=value)
        except ConfirmationCode.DoesNotExist:
            raise ValidationError('Invalid confirmation code.')
        return value
