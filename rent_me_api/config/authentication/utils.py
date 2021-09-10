from django.core.mail import EmailMessage

class Util:
    
    # use a static method so we don't need to instantiate the Util class before using it
    @staticmethod
    def send_email(data):
        
        email = EmailMessage(
            subject=data['email_subject'], 
            body=data['email_body'],
            to=[data['send_to']]
        )
        email.send()