from django.db import models

# Create your models here.
class Transaction(models.Model):
    amount = models.IntegerField()
    currency = models.CharField(max_length=3)
    sender_name = models.CharField(max_length=80)
    receiver_bank = models.CharField(max_length=80)
    receiver_accoutnum = models.IntegerField()
    receiver_email = models.EmailField(max_length=255)
    transaction_status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=50)
    transaction_ref = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
        
        
        