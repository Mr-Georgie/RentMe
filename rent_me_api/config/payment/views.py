from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import response, status
import json

# Create your views here.
from products.models import Products
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer 
from django.http import HttpResponsePermanentRedirect

from django.conf import settings
from . import reloadly, flutterwave

import requests
import random
import string

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ['http', 'https']

def getPassword(length):
    """Generate a random string"""
    str = string.hexdigits
    return ''.join(random.choice(str) for i in range(length))
  

class PaymentTemplateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'
    public_key = settings.RAVE_PUBLIC_KEY
        
    def get(self, request):
        amount = request.GET.get('amount')
        currency = request.GET.get('currency')
        country = request.GET.get('country')
        email = request.GET.get('email')
        phone_number = request.GET.get('phone_number')
        name = request.GET.get('name')
        receiver_email = request.GET.get('receiver_email')
        receiver_bank_accountnum = request.GET.get('receiver_bank_accountnum')
        receiver_bank_name = request.GET.get('receiver_bank_name')
        merchant_ref = request.GET.get('merchant_ref')
        
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
                'merchant_ref': merchant_ref
            }
        )
        
class PaymentAPIView(APIView):
    
    def post(self, request):
        resp = request.data
        # print(resp)
        amount = resp['amount']
        currency = resp['currency']
        country = resp['country']
        email = resp['email']
        phone_number = resp['phone_number']
        name = resp['name']
        receiver_email = resp['receiver_email']
        receiver_bank_accountnum = resp['receiver_bank_accountnum']
        receiver_bank_name = resp['receiver_bank_name']
        
        merchant_ref = getPassword(32)
        # fallback_url = 'http://127.0.0.1:8000/payment-page/flutterwave/'
        fallback_url = 'https://rent-me-api.herokuapp.com/payment-page/flutterwave/'
        
        
        return HttpResponseRedirect(redirect_to=fallback_url + (f'?amount={amount} &currency={currency}'
                                    f'&country={country}&email={email}&phone_number={phone_number}'
                                    f'&name={name}&receiver_email={receiver_email}'
                                    f'&receiver_bank_accountnum={receiver_bank_accountnum}&merchant_ref={merchant_ref}' 
                                    f'&receiver_bank_name={receiver_bank_name}'))
        
        
class SuccessTemplateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'success.html'
    secret_key = settings.RAVE_SECRET_KEY
        
    def get(self, request):
        sender_name = request.GET.get('customer')
        transaction_status = request.GET.get('status')
        transaction_id = request.GET.get('transcId')
        transaction_ref = request.GET.get('transcRef')
        receiver_info = request.GET.get('receiver_info').split()
        receiver_bank = receiver_info[0]
        receiver_accnum = receiver_info[1]
        receiver_mail = receiver_info[2]
        
        
        reloadly_access_token = reloadly.get_authenticated()['access_token']
        resp = flutterwave.verify_transaction(transaction_id, self.secret_key)
        
        if resp['status'] == 'success':
            amount = request.GET.get('amount')
            currency = request.GET.get('currency')
            
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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'error.html'
    
    def get(self, request):
        return Response({
            'message': 'transaction was not successful'
        })
        
class DemoTemplateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'demo.html'
    
    def get(self, request):
        return Response({
            'message': 'This is a demo page to test out payment'
        })