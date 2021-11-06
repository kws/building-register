import logging

from django.contrib.auth import get_user_model
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout as auth_logout

from register.util.tokens.resolver import token_services, get_token_method

User = get_user_model()

logger = logging.getLogger(__name__)


def login(request):
    return render(request, 'register/login.html', dict(methods=token_services))


def logout(request):
    auth_logout(request)
    return redirect("index")


def login_form(request, method):
    method = get_token_method(method)
    if not method:
        return HttpResponseNotFound('<h1>Login method not found</h1>')

    return method.handle_request(request)
