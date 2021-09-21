from django.core.mail import EmailMessage
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Email, To

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
        
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        from_email = Email('niyitegekah2021@gmail.com')
        to_email = [data['send_to']]
        subject = data['email_subject']
        content = Content("text/plain", data['email_body'])
        mail = Mail(from_email, to_email, subject, content)
        
        try:
            response = sg.client.mail.send.post(request_body=mail.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
        
        # email = EmailMessage(
        #     subject=data['email_subject'], 
        #     body=data['email_body'],
        #     to=[data['send_to']]
        # )
        # email.send()
        # EmailThread(email.send()).start()


