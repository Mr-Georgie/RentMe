from rest_framework import serializers
from . import google, facebook
# twitterhelper
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    
    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except :
            serializers.ValidationError(
                "This token is invalid or expired. Please login again"
            )
            
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            
            raise AuthenticationFailed('oops, who are you?')
        
        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'
        
        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name
        )
        
        
class FacebookSocialAuthSerializer(serializers.Serializer):
    """ Handles ... """
    auth_token = serializers.CharField()
    
    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        # print(user_data)
        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider, 
                user_id=user_id, 
                email=email, 
                name=name
            )
        except Exception as e:
            # print(e)
            raise serializers.ValidationError(
                'This token is invalid or expired. Please login again'    
            )
            