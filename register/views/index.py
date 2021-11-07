import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from register.models import SignInRecord, AuditRecord

logger = logging.getLogger(__name__)


@transaction.atomic
def _handle_sign_in_out(request):
    signed_in = SignInRecord.objects.user(request.user).today().open()
    audit = AuditRecord.objects.create_from_request(request)
    action = request.POST.get('action')

    if action == "sign-in" and signed_in.count() == 0:
        SignInRecord.objects.create(user=request.user, sign_in=audit)
    elif action == "sign-out":
        signed_in.sign_out(audit)


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
