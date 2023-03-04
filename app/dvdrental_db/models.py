from django.db import models

# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    genre = models.CharField(max_length=70, blank=False, default='')
    rating = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200, blank=False, default='')
    year = models.IntegerField(max_length=70, blank=False)