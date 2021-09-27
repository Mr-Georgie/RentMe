from rest_framework import serializers
from .models import BillingInfo


class BillingInfoSerializer(serializers.ModelSerializer):
    # id = 
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = BillingInfo
        fields = '__all__'