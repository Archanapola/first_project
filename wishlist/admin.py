from django.contrib import admin

# Register your models here.
from .models import *
# admin.site.register(wishlistMainModel)
class wishlistMainModelAdmin(admin.ModelAdmin):
    list_display = ['owner']
admin.site.register(wishlistMainModel,wishlistMainModelAdmin)