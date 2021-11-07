from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from register.models import SignInRecord


@permission_required('register.view_report')
@never_cache
def report(request):
    todays_records = SignInRecord.objects.today().order_by("user__first_name", "user__last_name", "sign_in__timestamp")
    signed_in_records = todays_records.open()
    signed_out_records = todays_records.closed()

    return render(request, 'register/report.html', dict(
        todays_records=todays_records,
        signed_in_records=signed_in_records,
        signed_out_records=signed_out_records,
    ))