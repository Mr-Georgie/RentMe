from django.urls import path

from .views import CartAPIView, CartDetailsAPIView, GetUserCartItems

urlpatterns = [
    path('', CartAPIView.as_view(), name='cart-items'),
    path('user-cart-items', GetUserCartItems.as_view(), name='user-cart-list'),
    
    path('cart-details-edit/<int:id>', CartDetailsAPIView.as_view(), name='cart-details-edit'),
]