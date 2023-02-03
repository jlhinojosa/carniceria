from django.db import models

class LatestManager(models.Manager):

    def latest(self):
        print('manager')
        return super().get_queryset().latest()