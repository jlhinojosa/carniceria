from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('venues/create', views.venue_create, name='venue_create'),
    path('venues/details/<int:id>', views.venue_details, name='venue_details'),
    path('drawers/create/<int:venueId>', views.drawer_create, name='drawer_create'),
    path('drawers/open/<int:drawerId>', views.drawer_open, name='drawer_open'),
    path('drawers/close/<int:drawerId>', views.drawer_close, name='drawer_close'),
]

