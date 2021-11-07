from django.urls import path

from . import views
from .views import auth, report, profile

urlpatterns = [
    path('accounts/login/', auth.login, name='login'),
    path('accounts/logout/', auth.logout, name='logout'),
    path('accounts/login/<str:method>', auth.login_form, name='login_form'),

    path('profile', profile.profile, name='profile'),

    path('report', report.report, name='report'),

    path('', views.index, name='index'),
]
