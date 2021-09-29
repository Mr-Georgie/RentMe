from os import stat
from requests.api import get
from rest_framework import views, status
from rest_framework.response import Response
from user_dashboard.permissions import permissions

from drf_yasg.utils import swagger_auto_schema # to edit the VerifyEmail class
from drf_yasg import openapi
from .sender_details import get_sender_details
from .receiver_details import get_details

from .serializers import ReloadlySerializer, ReloadlyAcceptedParameterSerializer
from .reloadly import get_authenticated, topup_product_owner
import random, string, json

from .operators import get_operator
from .countries import get_countries
# Create your views here.

def generate_random_string(length):
    """Generate a random string"""
    str = string.hexdigits
    return ''.join(random.choice(str) for i in range(length))

class ReloadlyPaymentAPIView(views.APIView):
    """
    Once cash transfer from flutterwave is successful, this endpoint handles mobile airtime topup to product owner. The required field is specified below.
     
    """
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(request_body=ReloadlyAcceptedParameterSerializer)
    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data['product_id']
        sender_phone = request.data['sender_phone']
        sender_country = request.data['sender_country']
        
        print(product_id)
        print(sender_phone)
        sender = get_sender_details(user)
        receiver = get_details(product_id)
        
        if sender_phone == None or sender_phone == '':
            return Response({
                'message': 'Please provide your phone number to proceed'
            })
        
        # sender_phone = sender['phone_number']
        # sender_country = sender['country']
        receiver_country = receiver.get('country')
        receiver_phone = receiver.get('phone_number')
        amount = request.data['amount']
        
        reloadly_access_token = get_authenticated()['access_token']
        resp = get_countries(reloadly_access_token)
        
        receiver_iso = ""
        sender_iso = ""
        
        for country in resp:
            if country['name'] == receiver_country:
                receiver_iso = country['isoName']
            if country['name'] == sender_country:
                sender_iso = country['isoName'] 
                
        operator_id = get_operator(receiver_phone, receiver_iso, reloadly_access_token)
                
        get_response = topup_product_owner(generate_random_string(32), operator_id,receiver_phone, receiver_iso, amount, 
                                            sender_phone, sender_iso, reloadly_access_token)
        
        if "errorCode" in get_response.keys():
            return Response({
                'reloadly_response': "error",
                "errorCode": get_response["errorCode"],
                "message": get_response["message"]
            }, status=status.HTTP_400_BAD_REQUEST)   
        else:
            data = {
                "receiver_phone":receiver_phone,
                "sender_phone":sender_phone,
                "amount":amount,
                "operator_id":operator_id,
                "transaction_id": get_response["transactionId"],
                "operator_name": get_response["operatorName"]
            }
            
            serializer = ReloadlySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print('Successfully saved topup to database')
            else:
                print(serializer.errors)
            
            return Response({
                'reloadly_response': "success",
                'details': get_response
            }, status=status.HTTP_200_OK)
        
        
class GetSupportedCountries(views.APIView):
    
    def get(self, request):
        reloadly_access_token = get_authenticated()['access_token']
        resp = get_countries(reloadly_access_token)
        countries = []
        
        for country in resp:
            countries.append(country['name']) 
    
        
        return Response({
            'count': len(countries),
            'response': countries
        }, status=status.HTTP_200_OK)
