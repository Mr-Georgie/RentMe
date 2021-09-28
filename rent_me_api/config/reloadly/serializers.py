from django.db.models import fields
from rest_framework import serializers
from .models import ReloadlyData


class ReloadlySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReloadlyData
        fields = ['sender_phone', 'transaction_id', 'operator_id','operator_name', 'amount']
        
    def create(self, validated_data):
        return ReloadlyData.objects.create(**validated_data)
    
    