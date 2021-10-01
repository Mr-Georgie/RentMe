from django.shortcuts import render
from .serializers import UserProductSerializer, ProductUploadSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, ListAPIView 
from products.models import Products
from rest_framework import permissions, views, status
from .permissions import IsOwner
from .check_user_details import completed_profile
from rest_framework.response import Response
from pagination.paginationhandler import CustomPaginator
# Create your views here.

from authentication.models import User
from authentication.serializers import UserSerializer, ResetPasswordByEmailSerializer, SetNewPasswordSerializer, LogoutSerializer
from authentication.utils import send_email
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse # reverse is used to get url name from url path
import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponsePermanentRedirect
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema # to edit the VerifyEmail class
from drf_yasg import openapi

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ['http', 'https']
    
class UserProductCreate(views.APIView):
    """
    Allows an authenticated user to add product or property for rent. Content-type should be multipart form to allow for image file upload. Notifies app admin at the once image is added. 
    If user has not completed all fields in his profile details, he would be given an error e.g: "error": ["Please provide your bank name in your account page"]
    """
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    
    @swagger_auto_schema(request_body=ProductUploadSerializer)
    def post(self, request, format=None):
        user = request.user
        check = completed_profile(user)['is_profile_complete']
        
        if check is False:
            
            print("profile incomplete")
            return Response({
                'error': completed_profile(user)['message']
            }, status=status.HTTP_403_FORBIDDEN)
        
        else:
            serializer = ProductUploadSerializer(data=request.data, context = {'request': request})
            if serializer.is_valid():
                serializer.save()
                
                data = {
                    'email_body': '<h2> Hi Admin, a new product has been added by ' + request.user.email +'. Please verify </h2>',
                    'email_subject': 'Product Verification on Rent Me',
                    'send_to': 'george.isiguzo@yahoo.com'
                }
                
                send_email(data)
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserProductListAPIView(ListAPIView):
    """
    To view a json list of all products added by an authenticated user. Accepts page number and returns a pagination list too
    """
    serializer_class = UserProductSerializer
    queryset = Products.objects.order_by('id')
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class UserProductDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    Handles individual product edit and view. Uses product id as query parameter    
    """
    serializer_class = UserProductSerializer
    queryset = Products.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    lookup_field = "id"
    
    parser_classes = [MultiPartParser, FormParser]
    
    @swagger_auto_schema(request_body=UserProductSerializer)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
 
class EditUserDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    To edit and update the currently authenticated user account details. To be used together with the 'view user details' endpoint.
    """
    permisssion_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    
class ViewUserDetailsAPIView(ListAPIView):
    """
    To view the currently authenticated user account details. To be used together with the 'edit-update user details' endpoint.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)   
      
class ResetPasswordByEmail(GenericAPIView):
    """
    Handles reset password request when user supplies email. Sends request email to user.
    The frontend developer should supply a redirect url once the token is validated
    and a fallback_url if there was an error while validating token.
    """
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
            fallback_url = request.data.get('fallback_url', '')
                
            email_body =  {
                'message': 'Hello, \n  Please use link below to reset your password:',
                'link': abs_url + '?redirect_url=' + redirect_url + '&fallback_url=' + fallback_url
            }
                
            data = {
                'email_body': email_body['message'] + '\n' + email_body['link'],
                'email_subject': 'Reset your password',
                'send_to': user.email
            }
                
            send_email(data)
        
        return Response({
            'success': 'We have sent you a link to reset your password'
        }, status=status.HTTP_200_OK)
        
class PasswordTokenCheck(views.APIView):
    """
    Validates the token in the reset password email sent. It redirects the user to the set new password page created on the frontend.
    Sends a user_id and token as query parameters.
    """
    
    def get(self, request, user_id, token):
        
        redirect_url = request.GET.get('redirect_url')
        fallback_url = request.GET.get('fallback_url')
        
        try:
            id = smart_str(urlsafe_base64_decode(user_id))
            user = User.objects.get(id=id)
            # fallback_url = 'https://www.youtube.com'
            
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
    """
    The frontend developer will take the query parameters from the redirect_url (user_id & token).
    This endpoint will accept a POST request that has the user_id, token and new user password.
    If the user takes too long to reset password, the token expires and the user will have to make another rest password request.
    If the user inputs his previous password, an authentication failed message will be returned: 'Please use another password'
    """
    
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'success': True,
            'message': 'Password reset success'
        }, status=status.HTTP_200_OK)
 
class LogoutAPIView(GenericAPIView):
    """This receives an access token and adds it to blacklisted token. Therefore, the user will have to login again to create a new token that would be accepted"""
    
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
