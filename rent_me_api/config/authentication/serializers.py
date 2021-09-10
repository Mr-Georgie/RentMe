# This is not a defult file. It was created by developer

from rest_framework import serializers
from .models import User
from django.contrib import auth 
from rest_framework.exceptions import AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'products'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        max_length=40, min_length=8, write_only=True
    ) # write only set to true to prevent pasword from being seen on the frontend
    
    class Meta:
        model = User
        fields = ['id','email', 'username', 'password']
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        
        return attrs
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    
    class Meta:
        model = User
        fields = ['token']
        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=6)
    password = serializers.CharField(max_length=68,min_length=8, write_only=True)
    username = serializers.CharField(max_length=68,min_length=8, read_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User
        fields = ['email','password','username','tokens']
    
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        
        # authenticate user
        user = auth.authenticate(email=email, password=password)
        
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
        if not user.is_verified:
            raise AuthenticationFailed('Your email is not verified')
        
        
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }