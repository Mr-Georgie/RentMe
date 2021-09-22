# from config.authentication.renderers import UserRenderer
"""
my imports
"""
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import force_str, smart_str, smart_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from inspect import currentframe
# from django.shortcuts import redirect, render
# from rest_framework.serializers import Serializer
# from rest_framework.views import exception_handler, APIView

from rest_framework import exceptions, generics, status, views, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer
from .models import User
from .utils import Util
from .sendgrid import SendEmail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse # reverse is used to get url name from url path
from django.conf import settings
from .renderers import UserRenderer
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
from rest_framework_simplejwt.tokens import RefreshToken
import jwt 
from drf_yasg.utils import swagger_auto_schema # to edit the VerifyEmail class
from drf_yasg import openapi

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ['http', 'https']

# Create your views here.
class RegisterView(generics.GenericAPIView):
    
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer, )
    
    def post(self, request):
        user_info = request.data
        serializer = self.serializer_class(data=user_info)
        serializer.is_valid(raise_exception=True) # will call validate in RegisterSerializer
        serializer.save() # will call create
        
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        abs_url = 'http://' + current_site + relative_link + '?token=' + str(token)
        
        email_body =  {
            'message': 'Hi ' + user.username +'. Please use link below to verify your email:',
            'link': abs_url
        }
        
        data = {
            'email_body': email_body['message'] + '\n' + email_body['link'],
            'email_subject': 'Verify your email',
            'send_to': user.email
        }
        
        # Util.send_email(data)
        SendEmail(data)
        
        return Response(user_data, status=status.HTTP_201_CREATED)
        
class VerifyEmail(views.APIView):
    
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, 
                                            description='Description', type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            
            return Response({'message':'Email successfully activated'}, status=status.HTTP_200_OK)
        
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPIView(generics.GenericAPIView):
    
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AuthUserAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        serializer = RegisterSerializer(user)
        
        return Response(serializer.data)
    
    
    
    
    