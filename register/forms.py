from django import forms
from django.contrib.auth import get_user_model

from register.models import ContactDetails, ContactValidationCode

User = get_user_model()


class NoSpaceCharField(forms.CharField):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        if value is not None:
            value = value.replace(" ", "")
        return value


class RegisterForm(forms.Form):
    contact_value = NoSpaceCharField(max_length=200, min_length=5)

    def send_code(self, method):
        contact_value = self.cleaned_data['contact_value']
        details, created = ContactDetails.objects.get_or_create(value=contact_value, method=method)

        code = ContactValidationCode(details=details).generate_code()
        code.save()

        print(f"Sending code to {contact_value}: {code.code}")

        return details


class ContactDetailsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class SignInForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    code = NoSpaceCharField(max_length=6, min_length=6)



