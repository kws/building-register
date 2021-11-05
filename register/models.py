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


contact_methods = {
    ContactMethod.PHONE: dict(title="SMS", icon="smartphone", label="Mobile Number"),
    ContactMethod.EMAIL: dict(title="Email", icon="email", label="Email Address"),
}


class ContactValidationCode(models.Model):
    details = models.ForeignKey("ContactDetails", on_delete=models.CASCADE)
    code = models.IntegerField()
    expires = models.DateTimeField()

    def generate_code(self):
        self.code = 100000 + secrets.randbelow(900000)
        self.expires = now() + timedelta(minutes=15)
        return self


class ContactDetails(models.Model):
    value = models.CharField(max_length=200, unique=True)
    method = models.CharField(max_length=5, choices=ContactMethod.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def validate_code(self, code):
        try:
             model = ContactValidationCode.objects.get(details=self, code=code)
             model.delete()
             return True
        except:
            return False


class AuditRecord(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True)
    user_agent = models.CharField(max_length=255, null=True)

    def __str__(self):
        if self.ip:
            return f"{self.timestamp:%-d %b %Y %H:%M} ({self.ip})"
        return f"{self.timestamp}"


class SignInManager(models.QuerySet):
    def today(self):
        return self.filter(date=now())

    def open(self):
        return self.filter(sign_out__isnull=True)

    def closed(self):
        return self.filter(sign_out__isnull=False)

    def user(self, user):
        return self.filter(user=user)

    def sign_out(self, audit: AuditRecord):
        return self.update(sign_out=audit)


class SignInRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    sign_in = models.ForeignKey(AuditRecord, on_delete=models.CASCADE, related_name="sign_in")
    sign_out = models.ForeignKey(AuditRecord, on_delete=models.CASCADE, null=True, related_name="sign_out")

    objects = SignInManager().as_manager()

    class Meta:
        ordering = ["sign_in__timestamp"]
