from authentication.models import User # for demo purposes only

def get_sender_details(user):
    user_ = User.objects.get(id=user)
    
    sender = {
       'email': user_.email ,
       'phone_number': user_.phone_number,
       'user_name': user_.username,
       'country': user_.country
    }
    return sender