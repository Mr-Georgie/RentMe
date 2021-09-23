from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import response, status

# Create your views here.
from products.models import Products
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer
from .sender_details import get_sender_details
from .receiver_details import get_details
from django.http import HttpResponsePermanentRedirect

from drf_yasg.utils import swagger_auto_schema # to edit the VerifyEmail class
from drf_yasg import openapi

from django.conf import settings
from . import reloadly, flutterwave

import random, string, json

class CustomRedirect(HttpResponsePermanentRedirect):
    """ Allow request from both http (dev server) & https (live server) """
    allowed_schemes = ['http', 'https']

def getPassword(length):
    """Generate a random string"""
    str = string.hexdigits
    return ''.join(random.choice(str) for i in range(length))

class PaymentAPIView(APIView):
    """ 
    Requires authentication. Handles POST request from the frontend. Cannot be tested on the documentation.
    Redirects the user to the flutterwave checkout page.
    """
    
    serializer_class = TransactionSerializer
    
    @swagger_auto_schema(request_body=TransactionSerializer)
    def post(self, request):
        resp = request.data
        
        print(request.user)
        
        amount = resp['amount']
        currency = resp['currency']
        product_id = resp['product_id']
        
        merchant_ref = getPassword(32)
        # fallback_url = 'http://127.0.0.1:8000/payment-page/flutterwave/'
        fallback_url = 'https://rent-me-api.herokuapp.com/payment-page/flutterwave/'
        
        
        return HttpResponseRedirect(redirect_to=fallback_url + (f'?amount={amount} &currency={currency}'
                                    f'&product_id={product_id}&merchant_ref={merchant_ref}'))
  

class PaymentTemplateView(APIView):
    """
    The flutterwave Payment UI Generator. Receives request from the checkout endpoints
    """
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'
    public_key = settings.RAVE_PUBLIC_KEY
        
    def get(self, request):
        # user = request.user
        user = 1 # demo purposes
        product_id = request.GET.get('product_id')
        merchant_ref = request.GET.get('merchant_ref')
        amount = request.GET.get('amount')
        currency = request.GET.get('currency')
        
        sender = get_sender_details(user)
        receiver = get_details(product_id)
        
        email = sender['email']
        phone_number = sender['phone_number']
        name = sender['user_name']
        country = sender['country']
        receiver_email = receiver.get('email')
        receiver_bank_accountnum = receiver.get('bank_account_number')
        receiver_bank_name = receiver.get('bank_name')
        receiver_country = receiver.get('country')
        payment_method = receiver.get('payment_method')
        receiver_phone = receiver.get('phone_number')
        
        # print(request.GET)
        
        return Response(
            {
                'public_key': self.public_key,
                'amount': amount,
                'currency': currency,
                'country': country,
                'email': email,
                'phone_number': phone_number,
                'name': name,
                'receiver_email': receiver_email,
                'receiver_bank_accountnum': receiver_bank_accountnum,
                'receiver_bank_name': receiver_bank_name,
                'receiver_country': receiver_country,
                'merchant_ref': merchant_ref,
                'payment_method': payment_method,
                'receiver_phone': receiver_phone
            }
        )
        
        
class SuccessTemplateView(APIView):
    """
    A Success page to be shown after successful payment
    """
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'success.html'
    secret_key = settings.RAVE_SECRET_KEY
        
    def get(self, request):
        sender_info = request.GET.get('customer_info').split()
        sender_name = sender_info[0]
        sender_country = sender_info[2]
        sender_phone = sender_info[1]
        transaction_status = request.GET.get('status')
        transaction_id = request.GET.get('transcId')
        transaction_ref = request.GET.get('transcRef')
        payment_method = request.GET.get('payment_method')
        receiver_info = request.GET.get('receiver_info').split()
        receiver_bank = receiver_info[0]
        receiver_accnum = receiver_info[1]
        receiver_mail = receiver_info[2]
        receiver_country = receiver_info[3]
        receiver_phone = receiver_info[4]
        
        # print('check out: ', receiver_accnum, '', receiver_bank, '', receiver_mail)
        
        resp = flutterwave.verify_transaction(transaction_id, self.secret_key)
        
        if resp['status'] == 'success':
            amount = request.GET.get('amount')
            currency = request.GET.get('currency')
            
            if payment_method == "AIRTIME TOPUP":
                reloadly_access_token = reloadly.get_authenticated()['access_token']
                
                get_response = reloadly.topup_product_owner(getPassword(32),receiver_country, receiver_phone, 
                                        sender_country, sender_phone, reloadly_access_token)
            
            print('reloadly error: ',get_response)
            
            data = {
                'amount': amount,
                'currency': currency,
                'sender_name': sender_name,
                'receiver_bank': receiver_bank,
                'receiver_accoutnum': receiver_accnum,
                'receiver_email': receiver_mail,
                'transaction_status': transaction_status,
                'transaction_id': transaction_id,
                'transaction_ref': transaction_ref
            }
            
            serializer = TransactionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print('Successfully saved transaction to database')
            else:
                print(serializer.errors)
            
            return Response({
                'status': 'verified and successful',
                'message': "You'll receive the requested product in 30 minutes",
                'sender_name': sender_name
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'failed and could not be verified',
                'message': 'Please contact our help desk at help@rentmeapp.com',
                'sender_name': sender_name
            }, status=status.HTTP_200_OK)
          
        
class ErrorTemplateView(APIView):
    """
    An Error page when there is an error during payment
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'error.html'
    
    def get(self, request):
        return Response({
            'message': 'transaction was not successful'
        })
        
class DemoTemplateView(APIView):
    """
    Mimics a typical frontend 'Proceed to checkout page'. Cannot be tested from this api doc
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'demo.html'
    
    def get(self, request):
        return Response({
            'message': 'This is a demo page to test out payment'
        })