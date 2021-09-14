from django.shortcuts import render
from .serializers import UserProductSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from products.models import Products
from rest_framework import permissions, views, status
from .permissions import IsOwner
from rest_framework.response import Response
from pagination.paginationhandler import CustomPaginator
# Create your views here.

from authentication.models import User
from authentication.serializers import ResetPasswordByEmailSerializer, SetNewPasswordSerializer, LogoutSerializer
from authentication.utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse # reverse is used to get url name from url path
import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponsePermanentRedirect

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ['http', 'https']

class UserProductListAPIView(ListCreateAPIView):
    serializer_class = UserProductSerializer
    queryset = Products.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class UserProductDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProductSerializer
    queryset = Products.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    lookup_field = "id"
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
      
class ResetPasswordByEmail(GenericAPIView):
    serializer_class = ResetPasswordByEmailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
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
            redirect_url = request.data.get('redirect_url', '')
                
            email_body =  {
                'message': 'Hello, \n  Please use link below to reset your password:',
                'link': abs_url + '?redirect_url=' + redirect_url
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
        
class PasswordTokenCheck(views.APIView):
    def get(self, request, user_id, token):
        
        redirect_url = request.GET.get('redirect_url')
        
        try:
            id = smart_str(urlsafe_base64_decode(user_id))
            user = User.objects.get(id=id)
            fallback_url = 'http://127.0.0.1:8000/admin'
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                
                if len(redirect_url)>3:
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    """ Provide a fallback url in .env then change redirect_url"""
                    print('provide a fallback url')
                    return CustomRedirect(fallback_url + '?token_valid=False')
            
            if redirect_url and len(redirect_url)>3:
                return CustomRedirect(redirect_url + '?token_valid=True&?message=Credential is valid&?user_id='+user_id+'&?token='+ token)
            else:
                """ Provide a fallback url in .env then change redirect_url"""
                print('provide a fallback url')
                return CustomRedirect(fallback_url + '?token_valid=False')
            
            
        except DjangoUnicodeDecodeError as e:
            return CustomRedirect(redirect_url + '?token_valid=False')
            
class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'success': True,
            'message': 'Password reset success'
        }, status=status.HTTP_200_OK)
 
class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)