from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from register.forms import ContactDetailsForm


@login_required
@never_cache
def profile(request):
    if request.method == 'POST':
        form = ContactDetailsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ContactDetailsForm(instance=request.user)

    return render(request, 'register/profile.html', dict(form=form))
