# This is not a defult file. It was created by developer

from django.urls import path
from .views import RegisterView, VerifyEmail, LoginAPIView, PasswordTokenCheck, ResetPasswordByEmail, SetNewPasswordAPIView, LogoutAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('password-reset-request/', ResetPasswordByEmail.as_view(), name='password-reset-request'),
    path('password-reset-verify/<user_id>/<token>/', PasswordTokenCheck.as_view(), name='password-reset-verify'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('auth/refresh=token', TokenRefreshView.as_view(), name='refreshtoken'),
    
]

