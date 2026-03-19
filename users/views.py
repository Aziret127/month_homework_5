from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .seriallzers import RegistrationSerializers, ConfirmationCodeSerializer
from .models import ConfirmationCode
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class UserConfirmView(APIView):
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
        
        try:
        
            confirmation = ConfirmationCode.objects.get(code=code)
            user = confirmation.user
            
            user.is_active = True
            user.save()
            
            confirmation.delete()
            
            return Response(
                {"detail": "Аккаунт подтвержден."},
                status=status.HTTP_200_OK
            )
            
        except ConfirmationCode.DoesNotExist:
            return Response(
                {"error": "Неверный код."},
                status=status.HTTP_400_BAD_REQUEST
            )


class AuthorizationAPIew (APIView):
    def post (self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegistrationAPIew(APIView):
    def post(self, request):
        serializer = RegistrationSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        confirmation_code = user.confirmation_code
        
        return Response({'user': user.id, 'username': user.username,'message': f'Код подтверждения отправлен'},status=status.HTTP_201_CREATED)
