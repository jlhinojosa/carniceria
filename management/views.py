from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *

# Create your views here.
def dashboard(request):

    venues = Venue.objects.filter(owner=request.user.id)

    context = { 'venues' : venues }

    return render(request, 'home.html', context)

def venue_create(request):

    context = {}

    form = VenueForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        # save the form data to model
        instance = form.save(commit=False)
        user = request.user

        instance.owner = user
        instance.save()
        form.save_m2m()

        return HttpResponseRedirect(reverse('dashboard'))
    else: 
        context['form']= form
        return render(request, "venues/create.html", context)

def venue_details(request, id):

    venue = Venue.objects.get(id=id)
    context = {
        'venue': venue,
    }
    return render(request, 'venues/details.html', context)

def drawer_create(request, venueId):

    context = {}

    form = DrawerForm(request.POST or None, request.FILES or None, initial={'venue': venueId})
    if form.is_valid():
        # save the form data to model
        instance = form.save()

        return HttpResponseRedirect(reverse('venue_details', kwargs={'id': venueId}))
    else: 
        context['form']= form
        return render(request, "drawers/create.html", context)

def drawer_open(request, drawerId):

    drawer = Drawer.objects.get(id=drawerId)

    if(drawer.status != 'Open'):
        drawer.status = 'Open'
        drawer.save()
    
    return HttpResponseRedirect(reverse('venue_details', kwargs={'id': drawer.venue.id}))

def drawer_close(request, drawerId):

    drawer = Drawer.objects.get(id=drawerId)

    if(drawer.status == 'Open'):
        drawer.status = 'Closed'
        drawer.save()
    
    return HttpResponseRedirect(reverse('venue_details', kwargs={'id': drawer.venue.id}))
