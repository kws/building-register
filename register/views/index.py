import logging

from django import dispatch
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from register.models import SignInRecord, AuditRecord

logger = logging.getLogger(__name__)

user_signed_in = dispatch.Signal()
user_signed_out = dispatch.Signal()


@transaction.atomic
def _handle_sign_in_out(request):
    signed_in = SignInRecord.objects.user(request.user).today().open()
    audit = AuditRecord.objects.create_from_request(request)
    action = request.POST.get('action')

    if action == "sign-in" and signed_in.count() == 0:
        SignInRecord.objects.create(user=request.user, sign_in=audit)
        user_signed_in.send_robust(sender=SignInRecord, request=request, user=request.user, audit=audit)
    elif action == "sign-out":
        signed_in.sign_out(audit)
        user_signed_out.send_robust(sender=SignInRecord, request=request, user=request.user, audit=audit)


@login_required
@never_cache
def index(request):
    if request.method == 'POST':
        _handle_sign_in_out(request)

    todays_records = SignInRecord.objects.user(request.user).today()
    signed_in_records = todays_records.open()

    return render(request, 'register/index.html', dict(
        todays_records=todays_records,
        signed_in_records=signed_in_records,
        user=request.user,
    ))
