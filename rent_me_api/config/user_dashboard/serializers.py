from django.db.models import fields
from rest_framework import serializers
from products.models import Products

class UserProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Products
        fields = ['id','name', 'description', 'price', 'category', 'on_loan', 'image'] 
        
    
class ProductUploadSerializer(serializers.ModelSerializer):
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Products
        fields = ['id','name', 'description', 'price','owner', 'category', 'on_loan', 'image'] 