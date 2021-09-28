from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=True)
    currency = serializers.CharField(required=True)
    product_id = serializers.IntegerField(required=True)
    transaction_status = serializers.CharField(max_length=20)
    transaction_id = serializers.CharField(max_length=50)
    transaction_ref = serializers.CharField(max_length=150)
        
        
    class Meta:
        model = Transaction
        fields = ['amount', 'currency', 'product_id', 'transaction_status', 'transaction_id', 'transaction_ref']
        
    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)