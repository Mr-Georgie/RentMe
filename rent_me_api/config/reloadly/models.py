from django.db import models

# Create your models here.
class ReloadlyData(models.Model):
    receiver_phone = models.CharField(max_length=20)
    sender_phone = models.CharField(max_length=20)
    operator_id = models.CharField(max_length=6)
    transaction_id = models.CharField(max_length=20)
    operator_name = models.CharField(max_length=20)
    amount = models.CharField(max_length=20)