from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django import forms
#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from datetime import date

# Create your models here.

class Family(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.code

class Subfamily(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.code

class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    def __unicode__(self):
        return self.name

class Machine(models.Model):
    machine_number = models.PositiveIntegerField(primary_key=True)
    family = models.ForeignKey(Family, on_delete=models.PROTECT)
    subfamily = models.ForeignKey(Subfamily, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    hourmeter_base = models.PositiveIntegerField()
    odometer_base = models.PositiveIntegerField()
    def __unicode__(self):
        return str(self.machine_number)

class WorkType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    def __unicode__(self):
        return self.name

class WorkOrder(models.Model):
    order_number = models.PositiveIntegerField(primary_key=True)
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    work_type = models.ForeignKey(WorkType, on_delete=models.PROTECT)
    in_datetime = models.DateTimeField()
    out_datetime = models.DateTimeField(null=True, blank=True)
    mechanic = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='mechanic')
    team_leader = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='team_leader')
    def __unicode__(self):
        return u'%s for %s by %s %s' % (self.work_type.name, self.machine_number, self.mechanic, self.out_datetime)

class SparePart(models.Model):
    factory_number = models.PositiveIntegerField(null=True, blank=True, unique=True)
    sage_number = models.PositiveIntegerField(null=True, blank=True, unique=True)
    spare_part_type = models.CharField(max_length=100)
    def clean(self):
        if self.factory_number == None and self.sage_number is None:
            raise forms.ValidationError('Field factory_number or sage_number required.')
    def __unicode__(self):
        return u'%s | P/N Fabrica: %s | P/N Sage: %s' % (self.spare_part_type, self.factory_number, self.sage_number)

class MachineSparePart(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    spare_part = models.ForeignKey(SparePart, on_delete=models.PROTECT)
    level = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    class Meta:
        unique_together = ('machine_number', 'spare_part', 'level')
    def __unicode__(self):
        return '%s Level %s: %s x%s' % (self.machine_number, self.level, self.spare_part.spare_part_type, self.quantity)

class SparePartHistoricPrice(models.Model):
    spare_part = models.ForeignKey(SparePart, on_delete=models.PROTECT)
    date = models.DateField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    def __unicode__(self):
        return str(self.spare_part)

class Input(models.Model):
    input_type = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=100)
    def __unicode__(self):
        return self.input_type

class MachineInput(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    input_number = models.ForeignKey(Input, on_delete=models.PROTECT)
    level = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    class Meta:
        unique_together = ('machine_number', 'input_number', 'level')
    def __unicode__(self):
        return '%s Level %s: %s x%s' % (self.machine_number, self.level, self.input_number.description, self.quantity)

class InstructionType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    def __unicode__(self):
        return self.name

class Instruction(models.Model):
    instruction_type = models.ForeignKey(InstructionType, on_delete=models.PROTECT)
    description = models.CharField(max_length=100)
    def __unicode__(self):
        return self.description

class MachineInstruction(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    instruction_number = models.ForeignKey(Instruction, on_delete=models.PROTECT)
    level = models.PositiveIntegerField()
    class Meta:
        unique_together = ('machine_number', 'instruction_number', 'level')
    def __unicode__(self):
        return '%s Level %s: %s' % (self.machine_number, self.level, self.instruction_number.description)

class Airport(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.code

class Inventory(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    purchase_value = models.DecimalField(max_digits=9, decimal_places=2)
    up_date = models.DateField()
    down_date = models.DateField(null=True, blank=True)
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT)
    annex = models.FileField(blank=True)
    def __unicode__(self):
        return str(self.machine_number)

class Hourmeter(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    datetime = models.DateTimeField()
    hourmeter_to_date = models.PositiveIntegerField()

class Odometer(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    datetime = models.DateTimeField()
    odometer_to_date = models.PositiveIntegerField()

class Status(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    def __unicode__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    def __unicode__(self):
        return self.name

class Profile(models.Model):
    bp = models.PositiveIntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    def __unicode__(self):
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
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    datetime = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.PROTECT)
    def __unicode__(self):
        return '%s | %s' % (self.machine_number, self.date)

'''
class PurchaseOrder(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.PROTECT)
    spare_part = models.ForeignKey(SparePart, on_delete=models.PROTECT)
    unit_cost = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField()
    def __unicode__(self):
        return str(self.work_order)
'''
