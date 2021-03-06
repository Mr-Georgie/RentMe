from django.core.mail import EmailMessage

import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()

class Util:
    
    # use a static method so we don't need to instantiate the Util class before using it
    @staticmethod
    def send_email(data):
        
        email = EmailMessage(
            subject=data['email_subject'],
            from_email='niyitegekah@gmail.com', 
            body=data['email_body'],
            to=[data['send_to']]
        )
        # email.send()
        EmailThread(email).start()