import logging

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout as auth_logout
from django.views.decorators.cache import never_cache

from register.util.tokens.resolver import token_services, get_token_method

User = get_user_model()

logger = logging.getLogger(__name__)


@never_cache
def login(request):
    return render(request, 'register/login.html', dict(methods=token_services))


@never_cache
def logout(request):
    auth_logout(request)
    return redirect("index")


@never_cache
def login_form(request, method):
    method = get_token_method(method)
    if not method:
        return HttpResponseNotFound('<h1>Login method not found</h1>')

    return method.handle_request(request)
