from enum import Enum

from django.db import models

from django.contrib.auth.models import User

from django.utils.translation import gettext as _

from .managers import *

# Create your models here.
DENOMINATION_TYPE = (
    ('Bill', _('Bill')),
    ('Coin', _('Coin'))
)

class Denomination(models.Model):

    value = models.DecimalField(max_digits=5, decimal_places=0)
    name = models.CharField(max_length=10, null=True, blank=True)
    currency = models.CharField(max_length=3, default='CLP')
    type =  models.CharField(
        max_length = 4,
        choices = DENOMINATION_TYPE
    )
    displayOrder = models.IntegerField()

class Company(models.Model):

    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200, null=True)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('venue_details', kwargs={'pk': self.pk})

class Venue(models.Model):

    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('venue_details', kwargs={'pk': self.pk})

DRAWER_STATUS = (
    ('New', _('New')),
    ('Open', _('Open')),
    ('Closed', _('Closed'))
)

class Drawer(models.Model):

    name = models.CharField(max_length=30)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=False)
    status =  models.CharField(
        max_length = 10,
        choices = DRAWER_STATUS,
        default = 'New'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_venue', kwargs={'pk': self.pk})

BALANCE_STATUS = (
    ('Confirmed', _('Confirmed')),
)

class ClosingBalance(models.Model):

    totalCashAmount = models.DecimalField(max_digits=10, decimal_places=0)
    dateTime = models.DateTimeField()
    status =  models.CharField(
        max_length = 10,
        choices = BALANCE_STATUS,
        default = 'Confirmed'
    )
    totalCarnes = models.DecimalField(max_digits=10, decimal_places=0)
    totalGetnet = models.DecimalField(max_digits=10, decimal_places=0)
    drawer = models.ForeignKey(Drawer, on_delete=models.CASCADE, null=False)

    objects = models.Manager()
    last = LatestManager()

class ClosingBalanceDetail(models.Model):

    balance = models.ForeignKey(ClosingBalance, on_delete=models.CASCADE, null=False)
    denomination = models.ForeignKey(Denomination, on_delete=models.CASCADE, null=False)
    totalAmount = models.DecimalField(max_digits=7, decimal_places=0)
