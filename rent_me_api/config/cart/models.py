from django.db import models
from authentication.models import User

# Create your models here.
class Cart(models.Model):
    
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.URLField()
    quantity = models.PositiveIntegerField(default=1)
    
# class CartItems(models.Model):
    