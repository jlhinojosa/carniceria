from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *

# Create your views here.
def home(request):

    if(request.user and request.user.is_authenticated):
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'home.html')

@login_required
def dashboard(request):
    venues = Venue.objects.filter(owner=request.user.id)

    context = { 'venues' : venues }

    return render(request, 'dashboard.html', context)

@login_required
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

@login_required
def venue_details(request, id):

    venue = Venue.objects.get(id=id)
    context = {
        'venue': venue,
    }
    return render(request, 'venues/details.html', context)

@login_required
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

@login_required
def drawer_open(request, drawerId):

    drawer = Drawer.objects.get(id=drawerId)

    if(drawer.status != 'Open'):
        drawer.status = 'Open'
        drawer.save()
    
    return HttpResponseRedirect(reverse('venue_details', kwargs={'id': drawer.venue.id}))

@login_required
def drawer_close(request, drawerId):

    context = {}

    form = DrawerClosingForm(request.POST or None, initial={'drawer': drawerId})    
    if form.is_valid(): 
        drawer = Drawer.objects.get(id=drawerId)
        drawer.status = 'Closed'
        drawer.save()
        form.save()
        return HttpResponseRedirect(reverse('venue_details', kwargs={'id': drawer.venue.id}))
    else:
        context['form'] = form
        return render(request, 'drawers/close.html', context)

