from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('register/submit', views.register_submit, name='register_submit'),
    path('register/<str:method>', views.register_mode, name='register_mode'),

    path('', views.index, name='index'),
]
