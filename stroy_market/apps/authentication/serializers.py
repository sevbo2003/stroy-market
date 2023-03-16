from rest_framework import serializers
from apps.authentication.models import User, PhoneToken
from apps.authentication.validators import validate_uzb_phone_number


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password', 'full_name']
        write_only_fields = ['password', 'username']
    

    def validate(self, attrs):
        data = super().validate(attrs)
        validate_uzb_phone_number(data.get('username', None))
        return data
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class PhoneTokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneToken
        fields = ['phone_number']

    def validate(self, attrs):
        data = super().validate(attrs)
        validate_uzb_phone_number(data.get('phone_number', None))
        return data


class PhoneTokenVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneToken
        fields = ['phone_number', 'token']

    def validate(self, attrs):
        data = super().validate(attrs)
        validate_uzb_phone_number(data.get('phone_number', None))
        return data