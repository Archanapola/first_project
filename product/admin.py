from django.contrib import admin
from .models import *
# Register your models here.


class productMainModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description','price','unique_id']
admin.site.register(productMainModel,productMainModelAdmin)

class productImageModelAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']

admin.site.register(productImageModel, productImageModelAdmin)