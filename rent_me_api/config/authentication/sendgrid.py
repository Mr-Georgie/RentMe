#!/usr/bin/env python3

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def SendEmail(data):
    """ Send an email to the provided email addresses

    :param to_email = email to be sent to
    :returns API response code
    :raises Exception e: raises an exception """
    message = Mail(
        from_email = 'niyitegekah2021@gmail.com',
        to_emails = [data['send_to']],
        subject = data['email_subject'],
        html_content= f"<strong> {data['email_body']}" +
        '<a href=''https://github.com/cyberjive''>right here!</a></strong>')
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response Code: {code} ")
        print(f"Response Body: {body} ")
        print(f"Response Headers: {headers} ")
        print("Message Sent!")
        return str(response.status_code)
    except Exception as e:
        print("Error: {0}".format(e))
    return str(e)
