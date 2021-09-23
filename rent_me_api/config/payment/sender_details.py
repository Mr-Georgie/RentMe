from authentication.models import User # for demo purposes only

def get_sender_details(user):
   #  user_ = User.objects.get(id=user)
    
    sender = {
       'email': user.email ,
       'phone_number': user.phone_number,
       'user_name': user.username,
       'country': user.country
    }
    return sender