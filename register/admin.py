from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db import transaction

from .models import ContactDetails, ContactValidationCode, SignInRecord, AuditRecord

User = get_user_model()

@admin.action(description='Merge users')
def merge_users(modeladmin, request, queryset):
    queryset.update(status='p')


class AuditRecordAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'ip', 'user_agent')
    ordering = ('-timestamp',)


class ContactDetailsAdmin(admin.ModelAdmin):
    list_display = ('value', 'method', 'user')


class ContactValidationCodeAdmin(admin.ModelAdmin):
    list_display = ('details', 'expires')


class SignInAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'sign_in', 'sign_out')


@admin.action(description='Merge users')
@transaction.atomic
def merge_users(modeladmin, request, queryset):
    users = queryset.order_by("date_joined")
    first_user = users[0]
    remainder = users[1:]

    ContactDetails.objects.filter(user__in=remainder).update(user=first_user)
    SignInRecord.objects.filter(user__in=remainder).update(user=first_user)

    User.objects.filter(id__in=[r.id for r in remainder]).delete()


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    actions = [merge_users]


# Register your models here.
admin.site.register(ContactDetails, ContactDetailsAdmin)
admin.site.register(ContactValidationCode, ContactValidationCodeAdmin)
admin.site.register(SignInRecord, SignInAdmin)
admin.site.register(AuditRecord, AuditRecordAdmin)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



