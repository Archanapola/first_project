from django.contrib import admin

from .models import *

# Register your models here.
# class studentMainModelAdmin(admin.ModelAdmin):
#     list_display = ['name','dob','image','branch']
#
# admin.site.register(studentMainModel,studentMainModelAdmin)
#
# class studentMarksModelAdmin(admin.ModelAdmin):
#     list_display = ['student','marks','sem']
# admin.site.register(studentMarksModel,studentMarksModelAdmin)

#
# class studentMarksMainModelAdmin(admin.ModelAdmin):
#     list_display = ['student','marks']
# admin.site.register(studentMarksMainModel,studentMarksMainModelAdmin)


admin.site.register(studentMainModel)
admin.site.register(studentMarksModel)
admin.site.register(studentMarksMainModel)