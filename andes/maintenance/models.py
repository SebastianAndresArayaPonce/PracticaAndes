from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django import forms

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
    annex = models.FileField(blank=True)
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    work_type = models.ForeignKey(WorkType, on_delete=models.PROTECT)
    level = models.PositiveIntegerField(null=True, blank=True)
    in_datetime = models.DateTimeField()
    out_datetime = models.DateTimeField(null=True, blank=True)
    mechanic = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='mechanic')
    team_leader = models.ForeignKey(User, on_delete=models.PROTECT, related_name='team_leader')
    is_closed = models.BooleanField(default=False)
    def clean(self):
        if self.work_type.name == "Preventivo" and self.level == None:
            raise forms.ValidationError('Field level is required for this type of work')
    def __unicode__(self):
        return u'%s for %s by %s %s' % (self.work_type.name, self.machine_number, self.mechanic, self.out_datetime)

class WorkDescription(models.Model):
    description = models.CharField(max_length=100)
    def __unicode__(self):
        return self.description

class WorkOrderWorkDescription(models.Model):
    order_number = models.ForeignKey(WorkOrder, on_delete=models.PROTECT)
    id_work_description = models.ForeignKey(WorkDescription, on_delete=models.PROTECT)

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
    class Meta:
        unique_together = ('spare_part', 'date')
    def __unicode__(self):
        return '%s at %s cost $%s USD' % (self.spare_part.spare_part_type, self.date, self.price)

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
    instruction_type = models.ForeignKey(InstructionType, on_delete=models.PROTECT)
    class Meta:
        unique_together = ('machine_number', 'instruction_number', 'level')
    def save(self, *args, **kwargs):
        self.instruction_type = self.instruction_number.instruction_type
        super(MachineInstruction, self).save(*args, **kwargs)
    def __unicode__(self):
        return '%s Level %s: %s' % (self.machine_number, self.level, self.instruction_number.description)

class LubricationChart(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")
    def __unicode__(self):
        return self.name

class LubricationChartDescription(models.Model):
    lubrication_chart = models.ForeignKey(LubricationChart, on_delete=models.PROTECT)
    number = models.PositiveIntegerField()
    description = models.CharField(max_length=100)
    class Meta:
        unique_together = ('lubrication_chart', 'number')
    def __unicode__(self):
        return "%s %s" % (self.lubrication_chart, self.number)

class MachineLubricationChart(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    lubrication_chart = models.ForeignKey(LubricationChart, on_delete=models.PROTECT)
    level = models.PositiveIntegerField()
    class Meta:
        unique_together = ('machine_number', 'lubrication_chart', 'level')
    def __unicode__(self):
        return "%s Level %s: %s" % (self.machine_number, self.level, self.lubrication_chart)

class Airport(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.code

class Area(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    def __unicode__(self):
        return self.name

class Inventory(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    purchase_value = models.DecimalField(max_digits=9, decimal_places=2)
    up_date = models.DateField()
    down_date = models.DateField(null=True, blank=True)
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT)
    annex = models.FileField(blank=True)
    def __unicode__(self):
        return str(self.machine_number)

class Profile(models.Model):
    bp = models.PositiveIntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    def __unicode__(self):
        return self.user.username

class PurchaseOrder(models.Model):
    work_order = models.OneToOneField(WorkOrder, on_delete=models.PROTECT)
    estimate = models.FileField()
    def __unicode__(self):
        return str(self.work_order)
'''
class Hourmeter(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    datetime = models.DateTimeField()
    hourmeter_to_date = models.PositiveIntegerField()

class Status(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    def __unicode__(self):
        return self.name

class History(models.Model):
    machine_number = models.ForeignKey(Machine, on_delete=models.PROTECT)
    datetime = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.PROTECT)
    def __unicode__(self):
        return '%s | %s' % (self.machine_number, self.date)

'''
