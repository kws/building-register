import logging

from django.contrib.auth import get_user_model
from django.http import HttpResponseNotFound
from django.shortcuts import render

from register.util.tokens.resolver import token_services, get_token_method

User = get_user_model()

logger = logging.getLogger(__name__)


def register(request):
    return render(request, 'register/register.html', dict(methods=token_services))


def register_mode(request, method):
    method = get_token_method(method)
    if not method:
        return HttpResponseNotFound('<h1>Registration method not found</h1>')

    return method.handle_request(request)

#
# @transaction.atomic
# def register_submit(request):
#     details_pk = request.session['concat_details']
#     details = ContactDetails.objects.get(pk=details_pk)
#
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data['code']
#             if details.validate_code(code):
#                 login(request, details, form.cleaned_data['first_name'], form.cleaned_data['last_name'])
#                 return redirect('index')
#             else:
#                 form.add_error("code", "Code not found.")
#     else:
#         form = SignInForm()
#
#     return render(request, 'register/register_submit.html', dict(form=form, show_details=details.user is None))
