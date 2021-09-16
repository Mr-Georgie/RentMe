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
    
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    cart_items = openapi.Parameter('cart_items', in_=openapi.IN_QUERY, 
                                description='Description', type=openapi.TYPE_OBJECT)
    
    @swagger_auto_schema(manual_parameters=[cart_items])
    def post(self, request, *args, **kwargs):
        serializer = CartSerializer(
            data=json.loads(request.GET.get('cart_items')), # convert post data to json
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
    serializer_class = CartSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    
    def get_queryset(self):
        """
        This should return a list of all the items
        for the currently authenticated user
        """
        user = self.request.user
        return Cart.objects.filter(owner=user)


class CartDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartUpdateSerializer
    queryset = Cart.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    lookup_field = "id"
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
      
