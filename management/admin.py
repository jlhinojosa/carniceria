from django.contrib import admin

from .models import *
# Register your models here.
class DenominationAdmin(admin.ModelAdmin):
    list_display = ('id', 'value','type', 'displayOrder')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')

class VenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class DrawerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'venue')

admin.site.register(Denomination, DenominationAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Drawer, DrawerAdmin)
