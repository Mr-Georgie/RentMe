from django.db.models import fields
from rest_framework import serializers
from .models import Products

class AllProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Products
        fields = ['id','name', 'description', 'price', 'category', 'on_loan', 'image'] 
        