from django.db.models import fields
from rest_framework import serializers
from .models import ReloadlyData


class ReloadlySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReloadlyData
        fields = '__all__'
        
    def create(self, validated_data):
        return ReloadlyData.objects.create(**validated_data)
    
class ReloadlyAcceptedParameterSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)
    sender_phone = serializers.CharField(required=True)
    
    class Meta:
        model = ReloadlyData
        fields = ['amount', 'product_id', 'sender_phone']
    
    