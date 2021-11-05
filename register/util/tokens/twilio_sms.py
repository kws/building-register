from django.conf import settings
from django import forms
from twilio.base.exceptions import TwilioRestException

from register.util.tokens.abstract_service import PingPongTokenService, SendCodeForm


class TwilioCodeForm(SendCodeForm):
    contact_value = forms.CharField(max_length=15, label="Phone Number")


class TwilioSMSService(PingPongTokenService):
    code = "sms"
    icon = "smartphone"
    label = "Text Message"

    default_form = TwilioCodeForm

    @property
    def configured(self):
        return hasattr(settings, 'TWILIO_CLIENT')

    def validate_contact_value(self, form):
        contact_value = form.cleaned_data['contact_value']
        try:
            result = settings.TWILIO_CLIENT.lookups.phone_numbers(contact_value).fetch(country_code='gb')
            return result.phone_number
        except TwilioRestException as e:
            form.add_error("contact_value", "This does not appear to be a correctly formatted UK phone number")
            return None

    def send_code(self, request, code):
        settings.TWILIO_CLIENT.messages.create(
            body=f"Your Social Finance sign-in code is {code.code}",
            from_='SF-REG',
            to=code.details.value
        )
