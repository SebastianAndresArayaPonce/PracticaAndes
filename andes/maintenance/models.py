from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    machine_number = models.IntegerField()
    family = models.ForeignKey(Family, on_delete=models.PROTECT)
    subfamily = models.ForeignKey(Subfamily, on_delete=models.PROTECT)
    purchase_value = models.IntegerField()
    up_date = models.DateField()
    down_date = models.DateField(blank=True)
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT)
    annex = models.FileField(blank=True)
    def __str__(self):
        return str(self.machine_number)

class Status(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bp = models.PositiveIntegerField(unique=True)
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    def __str__(self):
        return self.user.username

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
    #print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    #print sender.profile
    #print instance
    #print kwargs
    #if created:
    #    Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    #instance.profile.save()

class History(models.Model):
    machine_number = models.IntegerField()
    date = models.DateField(default=date.today)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.machine_number)

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
    price = models.IntegerField()
    def __str__(self):
        return str(self.spare_part)

class PurchaseOrder(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.PROTECT)
    spare_part = models.ForeignKey(SparePart, on_delete=models.PROTECT)
    unit_cost = models.IntegerField()
    quantity = models.IntegerField()
    def __str__(self):
        return str(self.work_order)
