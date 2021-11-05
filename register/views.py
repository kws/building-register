import logging

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from register.forms import RegisterForm, SignInForm
from register.models import ContactMethod, ContactDetails

logger = logging.getLogger(__name__)

contact_methods = {
    ContactMethod.PHONE: dict(title="SMS", icon="smartphone", label="Mobile Number"),
    ContactMethod.EMAIL: dict(title="Email", icon="email", label="Email Address"),
}


def index(request):
    return render(request, 'register/index.html')


def register(request):
    return render(request, 'register/register.html', dict(methods=contact_methods))


def register_mode(request, method):
    method = ContactMethod(method)
    if not method:
        return HttpResponseNotFound('<h1>Registration method not found</h1>')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                details = form.send_code(method)
                request.session['concat_details'] = details.pk
                return redirect('register_submit')
            except:
                logger.exception("Failed to send contact code")
                form.add_error(None, "Invalid contact method")
    else:
        form = RegisterForm()
    return render(request, 'register/register_mode.html', dict(form=form, method_id=method, method=contact_methods[method]))


def register_submit(request):
    details_pk = request.session['concat_details']
    details = ContactDetails.objects.get(pk=details_pk)

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if details.validate_code(code):
                # Sign-in or create the current user
                print("Sign in successful!")
                return redirect('index')
            else:
                form.add_error("code", "Code not found.")
    else:
        form = SignInForm()

    return render(request, 'register/register_submit.html', dict(form=form, show_details=details.user is None))


