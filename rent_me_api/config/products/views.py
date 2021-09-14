from django.shortcuts import render
from .serializers import AllProductSerializer
from rest_framework.generics import RetrieveAPIView
from .models import Products
from rest_framework import views
from .permissions import IsOwner
from rest_framework.response import Response
from pagination.paginationhandler import CustomPaginator
# Create your views here.

class AllProductListAPIView(views.APIView):
    
    def get(self, request):
        products = Products.objects.all()
        
        paginator = CustomPaginator()
        response = paginator.generate_response(products, AllProductSerializer, request)
        return response
        
        # serializer = AllProductSerializer(products, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductDetailsAPIView(RetrieveAPIView):
    serializer_class = AllProductSerializer
    queryset = Products.objects.all()
    lookup_field = "id"
      
