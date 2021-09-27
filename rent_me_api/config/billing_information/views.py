from django.shortcuts import render
from rest_framework import generics, status, permissions, views
from .serializers import BillingInfoSerializer
from .models import BillingInfo
from user_dashboard.permissions import IsOwner
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema # to edit the VerifyEmail class
from drf_yasg import openapi

# Create your views here.
class BillingInfoAPIView(views.APIView):
    """
    Requires authentication. Returns 401 Unauthorized if user is not logged in.
    """
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    
    @swagger_auto_schema(request_body=BillingInfoSerializer)
    def post(self, request, *args, **kwargs):
        serializer = BillingInfoSerializer(
            data=request.data,
            context = {'request': request} # to enable api-view get current userid
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Billing information saved'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    

class GetBillingInfos(generics.ListAPIView):
    """
        This should return a list of all the saved billing information for the currently authenticated user
    """
    serializer_class = BillingInfoSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    
    def get_queryset(self):
        user = self.request.user
        return BillingInfo.objects.filter(owner=user)


class EditBillingInfoDetails(generics.RetrieveUpdateDestroyAPIView):
    """
        This is used to access a specific billing information by id for the currently authenticated user.
    """
    
    serializer_class = BillingInfoSerializer
    queryset = BillingInfo.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    lookup_field = "id"
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
      
