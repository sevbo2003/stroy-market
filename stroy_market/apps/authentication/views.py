from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from apps.authentication.models import User, PhoneToken
from apps.authentication.serializers import UserSerializer, PhoneTokenCreateSerializer, PhoneTokenVerifySerializer
from apps.authentication.utils import generate_token, verify_token
from apps.authentication.tasks import send_background_sms
from apps.authentication.utils import generate_token, verify_token


class PhoneTokenViewSet(viewsets.ModelViewSet):
    queryset = PhoneToken.objects.all()
    serializer_class = PhoneTokenCreateSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        token = generate_token(phone_number)
        message = "Sizning maxsus kodiz: {}".format(token)
        send_background_sms.apply_async((phone_number, message))
        return Response({'status': 'success'})

    @action(detail=False, methods=['post'])
    def verify(self, request, *args, **kwargs):
        serializer = PhoneTokenVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        token = serializer.validated_data.get('token')
        if verify_token(phone_number, token):
            return Response({'status': 'success'})
        return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)