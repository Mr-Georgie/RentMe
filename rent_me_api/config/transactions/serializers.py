from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=True)
    currency = serializers.CharField(required=True)
    product_id = serializers.IntegerField(required=True)
        
        
    class Meta:
        model = Transaction
        fields = '__all__'
        
    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)