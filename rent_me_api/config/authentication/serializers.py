# This is not a defult file. It was created by developer

from rest_framework import serializers
from .models import User
from django.contrib import auth 
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



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
    tokens = serializers.SerializerMethodField()
    
    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }
    
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
        
class ResetPasswordByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=5)
    
    class Meta:
        field = ['email']
        
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, 
                max_length=55, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    user_id = serializers.CharField(min_length=1, write_only=True)
    
    class Meta:
        fields = ['password', 'token', 'user_id']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            user_id = attrs.get('user_id')
            id = force_str(urlsafe_base64_decode(user_id))
            
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('Please use another password', 401) # beta code
            
            user.set_password(password)
            user.save()
            
            return (user)
        
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        
        return super().validate(attrs)
        
        
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        
        return attrs
    
    def save(self, **kwargs):
        
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
        