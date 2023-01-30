from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('venues/create', views.venue_create, name='venue_create'),
    path('venues/details/<int:id>', views.venue_details, name='venue_details'),
    path('drawers/create/<int:venueId>', views.drawer_create, name='drawer_create'),
]

