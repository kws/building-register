import secrets
from datetime import timedelta

from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class ContactValidationCodeManager(models.Manager):

    def create_code(self, details: "ContactDetails", expires: int = 15) -> "ContactValidationCode":
        return super().create(
            details=details,
            code=100000 + secrets.randbelow(900000),
            expires=now() + timedelta(minutes=expires)
        )

    def validate_code(self, details: "ContactDetails", code: int):
        try:
            instance = super().get(details=details, code=code)
            instance.delete()
            return True
        except ContactValidationCode.DoesNotExist:
            return False


class ContactValidationCode(models.Model):
    details = models.ForeignKey("ContactDetails", on_delete=models.CASCADE)
    code = models.IntegerField()
    expires = models.DateTimeField()

    objects = ContactValidationCodeManager()


class ContactDetails(models.Model):
    value = models.CharField(max_length=200)
    method = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = [['value', 'method']]

    def __str__(self):
        return f"[{self.id}]: {self.method}={self.value} ({self.user})"


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
        get_latest_by = ["sign_in__timestamp"]
        permissions = [("view_report", "Can view reports of all records")]
