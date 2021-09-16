from django.db.models import fields
from rest_framework.response import Response
from .models import Cart
from rest_framework import serializers, status
from products.serializers import AllProductSerializer
from products.models import Products

class CartSerializer(serializers.ModelSerializer):
    # id = 
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quantity = serializers.IntegerField(required=False)
    
    class Meta:
        model = Cart
        fields = ['id','owner','product_id','name','price','quantity']
        
    def validate_product_id(self, value):
        # print(Products.objects.filter(id=value).exists())
        if not Products.objects.filter(id=value).exists():
            raise serializers.ValidationError('This product was not found')
        return value
    
    
class CartUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Cart
        fields = ['id','owner','price','quantity']
        
        
    # def validate(self, attrs):
    #     try:
    #         # id = attrs.get('id')
    #         product_id = attrs.get('product_id')
    #         price = attrs.get('price')
    #         quantity = attrs.get('quantity')
    #         check_cart = Cart.objects.filter(product_id=product_id).exists()
            
    #         if check_cart:
    #             user_cart = Cart.objects.get(product_id=product_id)
    #             if not Products.objects.filter(id=product_id).exists():
    #                 raise serializers.ValidationError('This product was not found')
    #             else:
    #                 user_cart.quantity = quantity
    #                 user_cart.price = price
    #                 user_cart.save()
                
    #         return (user_cart)
        
    #     except Exception as err:
    #         raise Response({
    #             'error': err
    #         })