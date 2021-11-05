from django.contrib import admin

from .models import ContactDetails, ContactValidationCode

# Register your models here.
admin.site.register(ContactDetails)
admin.site.register(ContactValidationCode)

