from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register),
    path('logout', views.logout),
    path('login', views.login, name='login'),
]
