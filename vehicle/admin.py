from django.contrib import admin
from .models import *
# Register your models here.
class vehicleMainModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','vehicle_no','status','image' ]
admin.site.register(vehicleMainModel,vehicleMainModelAdmin)


class vehicleBreakdownModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'vehicle', 'status']

admin.site.register(vehicleBreakdownModel,vehicleBreakdownModelAdmin)


class vehicleBreakdownImageModelAdmin(admin.ModelAdmin):
    list_display = ['breakdown', 'image', 'status']

admin.site.register(vehicleBreakdownImageModel,vehicleBreakdownImageModelAdmin)
# admin.site.register(vehicleBreakdownImageModel)

class vehicleBreakdownAssignedModelAdmin(admin.ModelAdmin):
    list_display = ['breakdown', 'owner']

admin.site.register(vehicleBreakdownAssignedModel,vehicleBreakdownAssignedModelAdmin)
# admin.site.register(vehicleBreakdownAssignedModel)

class vehicleBreakdownInpectionModelAdmin(admin.ModelAdmin):
    list_display = ['breakdown', 'owner', 'reason', 'status']

admin.site.register(vehicleBreakdownInpectionModel,vehicleBreakdownInpectionModelAdmin)
# admin.site.register(vehicleBreakdownInpectionModel)
