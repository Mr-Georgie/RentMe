from django.db.models import fields
from rest_framework import serializers
from products.models import Products

class UserProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Products
        fields = ['id','name', 'description', 'price', 'category'] 