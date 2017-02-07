from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from datetime import date

# Create your models here.

class Family(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.code

class Subfamily(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.code

class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    def __str__(self):
        return self.name

class Machine(models.Model):
    machine_number = models.PositiveIntegerField(primary_key=True)
    family = models.ForeignKey(Family, on_delete=models.PROTECT)
    subfamily = models.ForeignKey(Subfamily, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    hourmeter_base = models.PositiveIntegerField()
    odometer_base = models.PositiveIntegerField()
    def __str__(self):
        return str(self.machine_number)

class WorkType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    def __str__(self):
        return self.name

class WorkOrder(models.Model):
    work_type = models.ForeignKey(WorkType, on_delete=models.PROTECT)
    datetime = models.DateTimeField()
    mechanic = models.ForeignKey(User, on_delete=models.PROTECT, related_name='mechanic')
    team_leader = models.ForeignKey(User, on_delete=models.PROTECT, related_name='team_leader')
    def __str(self):
        return str(self.work_type)

class SparePart(models.Model):
    factory_number = models.PositiveIntegerField(null=True, blank=True)
    sage_number = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=50, primary_key=True)
    def __str__(self):
        return self.name

class MachineSparePart(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    spare_part = models.ForeignKey(SparePart, on_delete=models.PROTECT)
    level = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

class SparePartHistoricPrice(models.Model):
    spare_part = models.ForeignKey(SparePart, on_delete=models.PROTECT)
    date = models.DateField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    def __str__(self):
        return str(self.spare_part)

class InputType(models.Model):
    input_type = models.CharField(max_length=50, primary_key=True)
    def __str__(self):
        return self.input_type

class Input(models.Model):
    input_type = models.ForeignKey(InputType, on_delete=models.PROTECT)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.input_type

class MachineInput(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    input_number = models.ForeignKey(Input, on_delete=models.PROTECT)
    level = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

class InstructionType(models.Model):
    instruction_type = models.CharField(max_length=50, primary_key=True)
    def __str__(self):
        return self.instruction_type

class Instruction(models.Model):
    instruction_type = models.ForeignKey(InstructionType, on_delete=models.PROTECT)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.instruction_type

class MachineInstruction(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    instruction_number = models.ForeignKey(Instruction, on_delete=models.PROTECT)
    level = models.PositiveIntegerField()

class Airport(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.code

class Inventory(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    purchase_value = models.DecimalField(max_digits=9, decimal_places=2)
    up_date = models.DateField()
    down_date = models.DateField(null=True, blank=True)
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT)
    annex = models.FileField(blank=True)
    def __str__(self):
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
    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    def __str__(self):
        return self.name

class Profile(models.Model):
    bp = models.PositiveIntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    datetime = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.PROTECT)
    def __str__(self):
        return '%s | %s' % (self.machine_number, self.date)

'''
class PurchaseOrder(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.PROTECT)
    spare_part = models.ForeignKey(SparePart, on_delete=models.PROTECT)
    unit_cost = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return str(self.work_order)
'''
