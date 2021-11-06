from django.urls import path

from . import views
from .views import auth

urlpatterns = [
    path('accounts/login/', auth.login, name='login'),
    path('accounts/logout/', auth.logout, name='logout'),
    path('accounts/login/<str:method>', auth.login_form, name='login_form'),

    path('', views.index, name='index'),
]
