from django.urls import path

from .views import UserProductDetailsAPIView,UserProductCreate, UserProductListAPIView, PasswordTokenCheck, ResetPasswordByEmail, SetNewPasswordAPIView, LogoutAPIView

urlpatterns = [
    path('products-create/', UserProductCreate.as_view(), name='user-products-create'),
    path('products-list/', UserProductListAPIView.as_view(), name='user-products-list'),
    path('product-details/<int:id>', UserProductDetailsAPIView.as_view(), name='user-product-details'),
    path('password-reset-request/', ResetPasswordByEmail.as_view(), name='password-reset-request'),
    path('password-reset-verify/<user_id>/<token>/', PasswordTokenCheck.as_view(), name='password-reset-verify'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]