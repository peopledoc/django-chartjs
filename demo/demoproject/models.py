from django.db import models


class Meter(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=255)
    reading = models.IntegerField()

    class Meta:
        ordering = ('-date', 'name')
