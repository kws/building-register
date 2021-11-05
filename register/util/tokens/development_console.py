from django.conf import settings
from django.contrib.auth import get_user_model
from register.util.tokens.abstract_service import SendCodeForm, PingPongTokenService

User = get_user_model()


class DevelopmentConsoleService(PingPongTokenService):
    code = "dev"
    icon = "engineering"
    label = "Development"

    @property
    def configured(self):
        return settings.DEBUG

    def validate_contact_value(self, form):
        contact_value = form.cleaned_data['contact_value']
        if contact_value == "fail":
            form.add_error("contact_value", "This is a sample validation error")
            return None
        return contact_value

    def send_code(self, request, code):
        print(f"Sending code {code.code} to {code.details.value}")