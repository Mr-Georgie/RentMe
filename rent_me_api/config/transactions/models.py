from django.db import models

# Create your models here.
class Transaction(models.Model):
    product_id = models.IntegerField()
    amount = models.IntegerField()
    currency = models.CharField(max_length=5)
    sender_name = models.CharField(max_length=80)
    receiver_bank = models.CharField(max_length=80)
    receiver_accout_number = models.CharField(max_length=50)
    receiver_email = models.EmailField(max_length=255)
    transaction_status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=50)
    transaction_ref = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
        
        
        