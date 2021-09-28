from products.models import Products
from authentication.models import User

def get_details(product_id):
    
    if Products.objects.filter(id=product_id).exists():
        product = Products.objects.get(id=product_id)
        product_owner_id = product.owner
        product_owner_details = User.objects.get(id=product_owner_id.id)
        
        return {
            'email': product_owner_details.email,
            'bank_account_number': product_owner_details.bank_account_number,
            'bank_name': product_owner_details.bank_name,
            'country': product_owner_details.country,
            'phone_number': product_owner_details.phone_number,
            'payment_method': product.payment_method
        }
    else:
        print('product does not exist')
        