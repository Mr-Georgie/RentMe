from django.db import models

# my imports
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken 

# Create your models here.

# Overwrite the default user model
class UserManager(BaseUserManager):
    
    # create user (Customer)
    def create_user(self, username, email, password=None):
        
        if username is None:
            raise TypeError('A user must a username')
        if email is None:
            raise TypeError('A user must an email')
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        
        return user
        
    # create super user (Admin)
    def create_superuser(self, username, email, password=None):
        
        if password is None:
            raise TypeError('Password must not be None')
        
                
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user

AUTH_PROVIDERS = {
    'facebook': 'facebook', 'twitter': 'twitter',
    'google': 'google', 'email':'email'
}

# Model for creating user fields
class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email')
    )
    
    # These fields are temporarily given default values until Frontend creates a UI for users to update their account details
    bank_account_number = models.CharField(max_length=20,blank=True, null=True, default="0059227130")
    bank_name = models.CharField(max_length=50, blank=True, null=True, default="Access")
    country = models.CharField(max_length=50, blank=True, null=True, default="Nigeria")
    phone_number = models.CharField(max_length=50, blank=True, null=True, default="08144149628")
    
    
    USERNAME_FIELD = 'email' # to enable login with email instead of username (default)
    REQUIRED_FIELDS = ['username']
    
    # important !
    objects = UserManager() # tell django how to manage update of type User
    
    def __str__(self):
        return self.email
    
    def tokens(self):
        token = RefreshToken.for_user(self)
        
        return {
            'refresh': str(token),
            'access': str(token.access_token)
        }
    
    