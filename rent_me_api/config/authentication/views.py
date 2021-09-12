# from config.authentication.renderers import UserRenderer
from inspect import currentframe
from django.shortcuts import render

# my imports
from rest_framework import exceptions, generics, status, views, permissions
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_simplejwt.tokens import RefreshToken 
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, ResetPasswordByEmailSerializer, SetNewPasswordSerializer, LogoutSerializer
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse # reverse is used to get url name from url path
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema # to edit the VerifyEmail class
from drf_yasg import openapi
from .renderers import UserRenderer

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse # reverse is used to get url name from url path


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
        
        Util.send_email(data)
        
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
    
class ResetPasswordByEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordByEmailSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        email = request.data['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user_id = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
                
            current_site = get_current_site(
                request=request).domain
            relative_link = reverse('password-reset-verify',kwargs={'user_id': user_id,'token': token})
            abs_url = 'http://' + current_site + relative_link
                
            email_body =  {
                'message': 'Hello, \n  Please use link below to reset your password:',
                'link': abs_url
            }
                
            data = {
                'email_body': email_body['message'] + '\n' + email_body['link'],
                'email_subject': 'Reset your password',
                'send_to': user.email
            }
                
            Util.send_email(data)
        
        return Response({
            'success': 'We have sent you a link to reset your password'
        }, status=status.HTTP_200_OK)
        
class PasswordTokenCheck(generics.GenericAPIView):
    def get(self, request, user_id, token):
        try:
            id = smart_str(urlsafe_base64_decode(user_id))
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'error':'Token is not valid, please request a new one'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({
                'success': True,
                'message':'Credential is valid',
                'user_id': user_id,
                'token': token
            }, status=status.HTTP_200_OK)
            
        except DjangoUnicodeDecodeError as e:
            return Response({
                'error':'Token is not valid, please request a new one'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'success': True,
            'message': 'Password reset success'
        }, status=status.HTTP_200_OK)
        
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
    
    
    