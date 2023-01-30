from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Venue(models.Model):

    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_venue', kwargs={'pk': self.pk})

class Drawer(models.Model):

    name = models.CharField(max_length=30)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_venue', kwargs={'pk': self.pk})
