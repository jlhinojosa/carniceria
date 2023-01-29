from django.contrib import admin

from .models import *
# Register your models here.

class VenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Venue, VenueAdmin)
