from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('venues/create', views.create_venue, name='create_venue'),
]

