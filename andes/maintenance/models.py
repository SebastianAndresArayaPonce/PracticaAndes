from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Family(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Subfamily(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Airport(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Inventory(models.Model):
    machine_number = models.IntegerField(default=0)
    family = models.ForeignKey(Family, on_delete=models.PROTECT)
    subfamily = models.ForeignKey(Subfamily, on_delete=models.PROTECT)
    purchase_value = models.IntegerField(default=0)
    up_date = models.DateField(default=date.today)
    down_date = models.DateField(null=True)
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT)
    annex = models.FileField(null=True)
    def __str__(self):
        return self.machine_number

class Status(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class History(models.Model):
    machine_number = models.IntegerField(default=0)
    date = models.DateField(default=date.today)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    def __str__(self):
        return self.machine_number

class Area(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
