from django.urls import path

from . import views
from .views import auth

urlpatterns = [
    path('accounts/login/', auth.register, name='register'),
    path('accounts/login/<str:method>', auth.register_mode, name='register_mode'),

    path('', views.index, name='index'),
]
