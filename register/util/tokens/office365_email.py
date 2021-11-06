import logging

from django.conf import settings
from django import forms
from django.template.loader import render_to_string

from register.util.tokens.abstract_service import PingPongTokenService, SendCodeForm

logger = logging.getLogger(__name__)


class EmailCodeForm(SendCodeForm):
    contact_value = forms.EmailField(max_length=100, label="Email Address")


class Office365EmailService(PingPongTokenService):
    code = "email"
    icon = "mail"
    label = "Email"

    default_form = EmailCodeForm

    try:
        __sender_name = settings.O365_EMAIL_SENDER
    except:
        __sender_name = None

    default_message = """
    You are registering using email. Please enter your email address to receive your one-time token.
    """

    validate_code_message = f"""
    Your code has now been sent. Keep a look out for a message from '{__sender_name}'.
    Please enter your code to log in.
    """

    validate_code_with_contact_message = f"""
    Your code has now been sent. Keep a look out for a message from '{__sender_name}'. 
    Please enter your name and code to set up your account.
    """

    @property
    def configured(self):
        return hasattr(settings, 'O365_EMAIL_SENDER')

    def send_code(self, request, code):
        body_content = render_to_string('register/login_message_email.html', dict(code=code.code))

        message = dict(
            subject="SF Building Sign-In Code",
            body=dict(contentType="HTML", content=body_content),
            toRecipients=[dict(emailAddress=dict(address=code.details.value))],
        )
        response = settings.MSGRAPHY_CLIENT.make_request(
            f"/users/{settings.O365_EMAIL_SENDER}/sendMail",
            method="POST",
            json=dict(message=message, saveToSentItems=False)
        )
        if not response.ok:
            logger.exception(f"Failed to send token message to {code.details.value}")
            raise Exception("Failed to send message")