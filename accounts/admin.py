from django.contrib import admin
from .models import *

# Register your models here.
class accountsUserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number','email']

admin.site.register(accountsUserModel,accountsUserModelAdmin)

# class accountsUserProfileModelAdmin(admin.ModelAdmin):
#     list_display = ['owner','name', 'dob', 'image']
#
# admin.site.register(accountsUserProfileModel,accountsUserProfileModelAdmin)
# class accountsUserProfileModelAdmin(admin.ModelAdmin):
#     list_display = ['name', 'dob','gender']
admin.site.register(accountsUserProfileModel)

class accountsUserLoginOtpModelAdmin(admin.ModelAdmin):
    list_display = ['owner', 'otp','active']
admin.site.register(accountsUserLoginOtpModel, accountsUserLoginOtpModelAdmin)

class accountsUserCartProductModelAdmin(admin.ModelAdmin):
    list_display = ['owner', 'product','product_status', 'status']
admin.site.register(accountsUserCartProductModel, accountsUserCartProductModelAdmin)

class accountsUserCartModelAdmin(admin.ModelAdmin):
    list_display = ['owner', 'price']
admin.site.register(accountsUserCartModel, accountsUserCartModelAdmin)
