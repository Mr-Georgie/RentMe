from django.db.models import fields
from rest_framework import serializers
from .models import ReloadlyData


class ReloadlySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReloadlyData
        fields = '__all__'
        
    def create(self, validated_data):
        return ReloadlyData.objects.create(**validated_data)
    
    