from django.shortcuts import render
from .serializers import AllProductSerializer
from rest_framework.generics import RetrieveAPIView
from .models import Products
from rest_framework import views, status
from .permissions import IsOwner
from rest_framework.response import Response
from pagination.paginationhandler import CustomPaginator
from rest_framework.parsers import MultiPartParser, FormParser
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
      

# class ProductUpload(views.APIView):
    
#     parser_classes = [MultiPartParser, FormParser]
    
#     def post(self, request, format=None):
#         print(request.data)
#         serializer = ProductUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
