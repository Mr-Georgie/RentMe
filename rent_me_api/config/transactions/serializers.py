from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = '__all__'
        
        
    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)


class TransactionsAcceptedParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'currency', 'product_id', 'transaction_status', 'transaction_id', 'transaction_ref']
        
        