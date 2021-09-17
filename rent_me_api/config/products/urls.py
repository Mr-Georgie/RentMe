from django.urls import path

from .views import AllProductListAPIView,  ProductDetailsAPIView

urlpatterns = [
    path('all-products-list/', AllProductListAPIView.as_view(), name='all-products-list'),
    path('product-details/<int:id>', ProductDetailsAPIView.as_view(), name='product-details')
]
