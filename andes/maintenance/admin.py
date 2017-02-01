from django.contrib import admin
from .models import Family, Subfamily, Airport, Inventory, Status, History, Area, WorkType, WorkOrder, SparePart, SparePartHistoricPrice, PurchaseOrder

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
