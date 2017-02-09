from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *

# Register your models here.
admin.site.register(Family)
admin.site.register(Subfamily)
admin.site.register(Category)
admin.site.register(Machine)
admin.site.register(SparePart)
admin.site.register(MachineSparePart)
admin.site.register(SparePartHistoricPrice)
admin.site.register(Input)
admin.site.register(MachineInput)
admin.site.register(InstructionType)
admin.site.register(Instruction)
admin.site.register(MachineInstruction)
admin.site.register(WorkType)
admin.site.register(WorkOrder)
admin.site.register(Airport)
admin.site.register(Inventory)
#admin.site.register(Status)
#admin.site.register(History)
#admin.site.register(Area)
#admin.site.register(PurchaseOrder)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
