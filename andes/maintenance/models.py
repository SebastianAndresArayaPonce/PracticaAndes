from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
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
    down_date = models.DateField(blank=True)
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT)
    annex = models.FileField(null=True)
    def __str__(self):
        return str(self.machine_number)

class Status(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

'''class User(AbstractBaseUser):
    bp = models.'''

class History(models.Model):
    machine_number = models.IntegerField(default=0)
    date = models.DateField(default=date.today)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.machine_number)

class Area(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class WorkType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class WorkOrder(models.Model):
    work_type = models.ForeignKey(WorkType, on_delete=models.PROTECT)
    date = models.DateField(default=date.today)
    #mechanic = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str(self):
        return str(self.work_type)

class SparePart(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class SparePartHistoricPrice(models.Model):
    spare_part = models.ForeignKey(SparePart, on_delete=models.PROTECT)
    date = models.DateField(default=date.today)
    price = models.IntegerField(default=0)
    def __str__(self):
        return str(self.spare_part)

class PurchaseOrder(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.PROTECT)
    spare_part = models.ForeignKey(SparePart, on_delete=models.PROTECT)
    unit_cost = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return str(self.work_order)
