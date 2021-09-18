from django.db import models
from authentication.models import User
from django.utils.translation import gettext_lazy as _

def upload_to(instance, filename):
    return 'products/{filename}'.format(filename=filename)

# Create your models here.
class Products(models.Model):
    
    CATEGORY_OPTIONS = [
        ('GADGETS','GADGETS'),
        ('ELECTRONICS','ELECTRONICS'),
        ('AUTOMOBILE','AUTOMOBILE'),
        ('OFFICE SPACE','OFFICE SPACE'),
        ('AGRICULTURAL','AGRICULTURAL')
    ]
    
    name = models.CharField(max_length = 200)
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    on_loan = models.BooleanField(default=False)
    image = models.ImageField(_('Image'), upload_to=upload_to, default='products/default.jpg')
    is_verified = models.BooleanField(default=False)