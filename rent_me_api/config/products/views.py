from django.shortcuts import render
from .serializers import AllProductSerializer
from rest_framework.generics import RetrieveAPIView
from .models import Products
from rest_framework import views, status, generics
from .permissions import IsOwner
from rest_framework.response import Response
from pagination.paginationhandler import CustomPaginator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.

class AllProductListAPIView(views.APIView):
    """
    Returns a paginated list of all products in database. Doesn't require authentication. This endpoint is for app visitors
    """
    def get(self, request):
        products = Products.objects.all()
        
        paginator = CustomPaginator()
        response = paginator.generate_response(products, AllProductSerializer, request)
        return response
        
        # serializer = AllProductSerializer(products, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductDetailsAPIView(RetrieveAPIView):
    """
    Gets a specific product in database by product id. Doesn't require authentication. This endpoint is for app visitors
    """
    
    serializer_class = AllProductSerializer
    queryset = Products.objects.all()
    lookup_field = "id"
      
class ProductCategoryList(views.APIView):
    """
    Returns an array of product categories. Doesn't require authentication.
    """
    
    serializer_class = AllProductSerializer
    products = Products.CATEGORY_OPTIONS
    categories = []
    
    def get(self, request):
        for product in self.products:
            if product[0] not in self.categories:
                self.categories.append(product[0])
        
        return Response({"categories": self.categories }, status=status.HTTP_200_OK)

class FilterByCategory(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = AllProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

class SearchByProductName(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = AllProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']