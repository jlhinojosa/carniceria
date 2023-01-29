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

def create_venue(request):

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