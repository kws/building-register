import secrets
from datetime import timedelta

from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class ContactMethod(models.TextChoices):
    EMAIL = 'email', _('EMail')
    PHONE = 'phone', _('Phone')


class ContactValidationCode(models.Model):
    details = models.ForeignKey("ContactDetails", on_delete=models.CASCADE)
    code = models.IntegerField()
    expires = models.DateTimeField()

    def generate_code(self):
        self.code = 100000 + secrets.randbelow(900000)
        self.expires = now() + timedelta(minutes=15)
        return self


class ContactDetails(models.Model):
    value = models.CharField(max_length=200)
    method = models.CharField(max_length=5, choices=ContactMethod.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def validate_code(self, code):
        try:
             model = ContactValidationCode.objects.get(details=self, code=code)
             model.delete()
             return True
        except:
            return False