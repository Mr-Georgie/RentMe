from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import TransactionSerializer, TransactionsAcceptedParameterSerializer
from .models import Transaction
from reloadly.sender_details import get_sender_details
from reloadly.receiver_details import get_details
from drf_yasg.utils import swagger_auto_schema # to edit the VerifyEmail class
from drf_yasg import openapi


# Create your views here.

class TransactionCreateAPIView(generics.GenericAPIView):
    """ 
    Saves successful transaction details to database.
    
    """
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(request_body=TransactionsAcceptedParameterSerializer)
    def post(self, request):
        user = request.user
        product_id = request.data['product_id']
        amount = request.data['amount']
        currency = request.data['currency']
        transaction_status = request.data['transaction_status']
        transaction_id = request.data['transaction_id']
        transaction_ref = request.data['transaction_ref']
        
        sender = get_sender_details(user)
        receiver = get_details(product_id)
        
        if sender['phone_number'] == None or sender['phone_number'] == '':
            return Response({
                'message': 'Please provide your phone number to proceed'
            })
        
        email = sender['email']
        sender_phone = sender['phone_number']
        sender_name = sender['user_name']
        receiver_mail = receiver['email']
        receiver_accnum = receiver.get('bank_account_number')
        receiver_bank = receiver.get('bank_name')
        receiver_country = receiver.get('country')
        payment_method = receiver.get('payment_method')
        receiver_phone = receiver.get('phone_number')
        amount = request.data['amount']
        
        data = {
                'product_id': product_id,
                'amount': amount,
                'currency': currency,
                'sender_name': sender_name,
                'receiver_bank': receiver_bank,
                'receiver_accout_number': receiver_accnum,
                'receiver_email': receiver_mail,
                'transaction_status': transaction_status,
                'transaction_id': transaction_id,
                'transaction_ref': transaction_ref
        }
        print(data['sender_name'])
        
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)

class TransactionBySender(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all the transactions
        for the currently authenticated user.
        """
        user = self.request.user
        return Transaction.objects.filter(sender_name=user)
    
class TransactionByReceiver(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all the transactions
        for the currently authenticated user.
        """
        user = self.request.user
        return Transaction.objects.filter(receiver_name=user)
            
            
            