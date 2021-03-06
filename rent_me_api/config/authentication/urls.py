# This is not a defult file. It was created by developer

from django.urls import path
from .views import RegisterView, VerifyEmail, LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('auth/refresh=token', TokenRefreshView.as_view(), name='refreshtoken'),
    
]

