from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.models import User
from django.forms.models import BaseInlineFormSet

from .models import *

# Register your models here.

class MachineInstructionAdmin(admin.ModelAdmin):
    fields = ['machine_number', 'instruction_number', 'level']

class UserProfileInlineFormSet(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                pass
        if count == 0:
            raise ValidationError('This fields are required.')

class UserProfileInline(admin.StackedInline):
    model = Profile
    extra = 1
    max_num = 1
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    template = 'admin/maintenance/stacked.html'
    formset = UserProfileInlineFormSet
    formset_required = True

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",)

    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("This field is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("This field is required.")
        return self.cleaned_data["last_name"]

class UserChangeForm(BaseUserChangeForm):
    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("This field is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("This field is required.")
        return self.cleaned_data["last_name"]

class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    add_form = UserCreationForm
    form = UserChangeForm
    inlines = (UserProfileInline, )

admin.site.register(Airport)
admin.site.register(Area)
admin.site.register(Category)
admin.site.register(Family)
admin.site.register(Input)
admin.site.register(InstructionType)
admin.site.register(Instruction)
admin.site.register(Inventory)
admin.site.register(LubricationChartDescription)
admin.site.register(LubricationChart)
admin.site.register(MachineInput)
admin.site.register(MachineInstruction, MachineInstructionAdmin)
admin.site.register(MachineLubricationChart)
admin.site.register(MachineSparePart)
admin.site.register(Machine)
admin.site.register(SparePartHistoricPrice)
admin.site.register(SparePart)
admin.site.register(Subfamily)
admin.site.register(WorkDescription)
admin.site.register(WorkOrderWorkDescription)
admin.site.register(WorkOrder)
admin.site.register(WorkType)
admin.site.register(PurchaseOrder)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
#admin.site.register(Status)
#admin.site.register(History)
