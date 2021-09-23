from django.shortcuts import render
from .serializers import CartSerializer, CartUpdateSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework import permissions, views, status, serializers
from .permissions import IsOwner
from rest_framework.response import Response
from .models import Cart
import json

from drf_yasg.utils import swagger_auto_schema # to edit the VerifyEmail class
from drf_yasg import openapi
# Create your views here.


class CartAPIView(views.APIView):
    """
    Requires authentication. Returns 401 Unauthorized if user is not logged in. The image field must be a valid url in database.
    Error response: 'This product already exists in cart. Update the product quantity instead'
    
    To update the product quantity, find the PUT endpoint below
    """
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    
    @swagger_auto_schema(request_body=CartSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CartSerializer(
            data=request.data,
            context = {'request': request} # to enable api-view get current userid
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Successfully added to cart'
            }, status=status.HTTP_201_CREATED)
        else:
            check_error = list(serializer.errors.values())[0][0] == 'cart with this product id already exists.'
            if check_error:
                return Response(
                {
                    'error': 'This product already exists in cart. Update the product quantity instead',
                    'status_code': 400                  
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
            else:
                return Response(
                    {'error': serializer.errors}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
    

class GetUserCartItems(ListAPIView):
    """
        This should return a list of all the items for the currently authenticated user
    """
    serializer_class = CartSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(owner=user)


class CartDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
        This is used to access a specific cart item by id for the currently authenticated user. Then, it can be retrieved, updated and deleted 
        based on the endpoints : GET, PUT, PATCH & DELETE
    """
    
    serializer_class = CartUpdateSerializer
    queryset = Cart.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    lookup_field = "id"
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
      
