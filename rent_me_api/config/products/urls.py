from django.urls import path

from .views import (AllProductListAPIView,  ProductDetailsAPIView, 
                    ProductCategoryList, FilterByCategory, SearchByProductName)

urlpatterns = [
    path('all-products-list/', AllProductListAPIView.as_view(), name='all-products-list'),
    path('product-details/<int:id>', ProductDetailsAPIView.as_view(), name='product-details'),
    path('all-categories/', ProductCategoryList.as_view(), name='all-categories'),
    path('filter-by-category/', FilterByCategory.as_view(), name='filter-by-category'),
    path('search-products/', SearchByProductName.as_view(), name='search-products')
]
