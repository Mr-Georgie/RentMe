from django.db import models
from authentication.models import User

# Create your models here.
class BillingInfo(models.Model):
    
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    country = models.CharField(max_length=50, blank=True, null=True)
    state =models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)