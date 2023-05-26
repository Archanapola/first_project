# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
# class o(admin.ModelAdmin):
#     list_display = ['id', 'phone_number','email']

# admin.site.register(orderMainModel)
class orderMainModelAdmin(admin.ModelAdmin):
    list_display = ['owner', 'final_price','status']
admin.site.register(orderMainModel,orderMainModelAdmin)