from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Family, Subfamily, Airport, Inventory, Status, History, Area, Profile, WorkType, WorkOrder, SparePart, SparePartHistoricPrice, PurchaseOrder

# Register your models here.
admin.site.register(Family)
admin.site.register(Subfamily)
admin.site.register(Airport)
admin.site.register(Inventory)
admin.site.register(Status)
admin.site.register(History)
admin.site.register(Area)
admin.site.register(WorkType)
admin.site.register(WorkOrder)
admin.site.register(SparePart)
admin.site.register(SparePartHistoricPrice)
admin.site.register(PurchaseOrder)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
