from django.db import models
from authentication.models import User

# Create your models here.
class Products(models.Model):
    
    CATEGORY_OPTIONS = [
        ('GADGETS','GADGETS'),
        ('ELECTRONICS','ELECTRONICS'),
        ('AUTOMOBILE','AUTOMOBILE'),
        ('AGRICULTURAL','AGRICULTURAL')
    ]
    
    name = models.CharField(max_length = 200)
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)