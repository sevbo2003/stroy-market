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
    

class MyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'full_name']


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)
        validate_uzb_phone_number(data.get('username', None))
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError('Passwords do not match')
        user = User.objects.filter(username=data.get('username')).first()
        if not user:
            raise serializers.ValidationError('User not found')
        if PhoneToken.objects.filter(phone_number=data.get('username'), is_verified=True).exists():
            return data
        raise serializers.ValidationError('Phone number is not verified')
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
    
    def create(self, validated_data):
        username = validated_data.get('username')
        user = User.objects.filter(username=username).first()
        user.set_password(validated_data.get('password'))
        user.save()
        return user