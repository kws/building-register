from django.contrib import admin

from .models import ContactDetails, ContactValidationCode, SignInRecord, AuditRecord


class ContactDetailsAdmin(admin.ModelAdmin):
    list_display = ('value', 'method', 'user')


class SignInAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'sign_in', 'sign_out')


# Register your models here.
admin.site.register(ContactDetails, ContactDetailsAdmin)
admin.site.register(ContactValidationCode)
admin.site.register(SignInRecord, SignInAdmin)
admin.site.register(AuditRecord)



