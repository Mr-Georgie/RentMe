# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def SendEmail(data):
    message = Mail(
        from_email='niyitegekah@gmail.com',
        to_emails=[data['send_to']],
        subject=data['email_subject'],
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)